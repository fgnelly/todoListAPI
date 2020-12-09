from data import User, AppSession
from utility.Security import encryptPassword, verifyPassword
from utility import SessionHandler
from utility.HttpException import HttpException, HttpErrorType, assertJSON

def Create(request):
    """
    @params: logintoken, name, username, password
    """
    requestJSON = request.get_json(silent=True)
    try:
        assertJSON(requestJSON, ['logintoken', 'name', 'username', 'password'])
        User.InputRuleSet.validateFromPropertyNames(['name', 'username', 'password'], requestJSON)

        with SessionHandler.app_and_db_session_scope(requestJSON['logintoken'], SessionHandler.PermissionLevel.ADMIN) as session:
            # check if same username already exists
            if User.loadFromDbByUsername(session.db_session, username=requestJSON['username']) is not None:
                raise HttpException(HttpErrorType.GenericError, 'User create', 'User with that username already exists in the database.')
            addedUser = User.addNew(session=session.db_session, name=requestJSON['name'], username=requestJSON['username'], password=encryptPassword(requestJSON['password']))
            return SessionHandler.OK(addedUser.toJSONObject())
    except HttpException as exc:
        return exc.GetResponse()

def Login(request, logger):
    """
    @params: username, password, [userAgent]
    """
    requestJSON = request.get_json(silent=True)
    try:
        assertJSON(requestJSON, ['username', 'password'])
        with SessionHandler.app_and_db_session_scope('', SessionHandler.PermissionLevel.NONE) as session:
            # here verify password and login are valid, create a session and return a token
            loadedUser = User.loadFromDbByUsername(session.db_session, username=requestJSON['username'])
            if not loadedUser:
                encryptPassword(requestJSON['password'])
            else:
                if(verifyPassword(requestJSON['password'], loadedUser.password)):
                    newSession = AppSession.addNewOrReturnLastIfValid(session.db_session, loadedUser.id, 1, requestJSON['userAgent'] if 'userAgent' in requestJSON else '')
                    return SessionHandler.OK({'logintoken': newSession.token})
            logger.error('Failed logon attempt for username: {}, from remote address: {}'.format(requestJSON['username'], str(request.remote_addr)))
            raise HttpException(HttpErrorType.GenericError, 'login', 'Invalid username or password.')
    except HttpException as exc:
        return exc.GetResponse()

def Logout(request):
    """
    @params: logintoken
    """
    requestJSON = request.get_json(silent=True)
    try:
        assertJSON(requestJSON, ['logintoken'])
        with SessionHandler.app_and_db_session_scope(requestJSON['logintoken'], SessionHandler.PermissionLevel.USER) as session:
            session.app_session.invalidate()
            return SessionHandler.OK()
    except HttpException as exc:
        return exc.GetResponse()