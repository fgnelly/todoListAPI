from data import AppSession, db_session_scope, User
from .HttpException import HttpException, HttpErrorType
import json
from enum import Enum

class PermissionLevel(Enum):
    NONE = 0
    USER = 1
    ADMIN = 2

def OK(json_data={}):
    json_data['success'] = True
    return json.dumps(json_data), 200, {'ContentType':'application/json'}

class AppSessionScope:
    def __init__(self, token, db_session, requiredPermissionLevel):
        loadedSession = AppSession.loadValidFromToken(db_session, token)
        # if requiredPermissionLevel == 0, then don't require a session object - just return a db_session (the app session will not be used anyway)
        if requiredPermissionLevel.value == 0:
            self.db_session = db_session
            return

        if loadedSession is None:
            raise HttpException(HttpErrorType.Unauthorized)
        else:
            loadedSession.updateLastUsed()
            
            if loadedSession.permissionLevel < requiredPermissionLevel.value:
                raise HttpException(HttpErrorType.NeedsPermission)
            self.app_session = loadedSession
            self.db_session = db_session
            self.current_user = User.loadFromDbById(db_session, uid=loadedSession.userid)

from contextlib import contextmanager
@contextmanager
def app_and_db_session_scope(token, requiredPermissionLevel):
    try:
        with db_session_scope() as db_session:
            yield AppSessionScope(token, db_session, requiredPermissionLevel)
    except Exception as exc:
        if isinstance(exc, HttpException):
            raise exc
        else:
            raise HttpException(HttpErrorType.GeneralConnectionError)