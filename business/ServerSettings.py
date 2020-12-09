from data import ServerSetting
from utility import SessionHandler
from utility.HttpException import HttpException, HttpErrorType, assertJSON

def GetPublicSetting(request):
    """
    @params: settingName
    """
    requestJSON = request.get_json(silent=True)
    try:
        assertJSON(requestJSON, ['settingName'])
        with SessionHandler.app_and_db_session_scope("", SessionHandler.PermissionLevel.NONE) as session:
            requestedSetting = ServerSetting.getByName(session.db_session, requestJSON['settingName'])
            if requestedSetting.count() > 0 and requestedSetting.first().isPublic:
                return SessionHandler.returnRequestOK(requestedSetting.first().toJSONObject())
            raise HttpException(HttpErrorType.NotFound, "GetPublicSetting", "Setting was not found.")
    except HttpException as exc:
        return exc.GetResponse()