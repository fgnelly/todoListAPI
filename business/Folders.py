from data import Folder
from utility import SessionHandler
from utility.HttpException import HttpException, HttpErrorType, assertJSON

def Create(request):
    """
    @params: logintoken, name, description
    """
    requestJSON = request.get_json(silent=True)
    try:
        assertJSON(requestJSON, ['logintoken', 'name', 'description'])
        Folder.InputRuleSet.validateFromPropertyNames(['name', 'description'], requestJSON)
        
        with SessionHandler.app_and_db_session_scope(requestJSON['logintoken'], SessionHandler.PermissionLevel.USER) as session:
            if Folder.getAllFromOwnerId(session.db_session, session.current_user.id).filter_by(name=requestJSON['name']).count() > 0:
                raise HttpException(HttpErrorType.GenericError, 'Folder Create', 'A folder with that name already exists in the database.')
            
            addedFolder = Folder.addNew(session=session.db_session, ownerid=session.current_user.id, name=requestJSON['name'], description=requestJSON['description'])
            return SessionHandler.returnRequestOK(addedFolder.toJSONObject())
    except HttpException as exc:
        return exc.GetResponse()

def GetAll(request):
    """
    @params: logintoken
    """
    requestJSON = request.get_json(silent=True)
    try:
        assertJSON(requestJSON, ['logintoken'])
        with SessionHandler.app_and_db_session_scope(requestJSON['logintoken'], SessionHandler.PermissionLevel.USER) as session:
            allFolders = Folder.getAllFromOwnerId(session.db_session, session.current_user.id)
            JSONFolders = [] if allFolders.count() == 0 else list(map(lambda x: x.toJSONObject(), allFolders))
            return SessionHandler.returnRequestOK({"folders": JSONFolders})
    except HttpException as exc:
        return exc.GetResponse()