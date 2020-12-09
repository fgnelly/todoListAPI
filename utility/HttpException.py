import json
from enum import Enum

def assertJSON(json, requiredKeys):
    if len(json.keys()) > 30:
        raise HttpException(HttpErrorType.BadJSON)
    if json is None:
        raise HttpException(HttpErrorType.BadJSON)
    for key in requiredKeys:
        if key not in json:
            raise HttpException(HttpErrorType.BadJSON)
    return True

class HttpErrorType(Enum):
    Unauthorized = {
        'code': 401,
        #'body': {'message': 'Not allowed :-('}
        'body': {'message': 'You gotta pay the troll toll to get in!'}
    }
    
    NeedsPermission = {
        'code': 403,
        'body': {'message': 'You need higher privelages to perform this action.'}
    }

    BadJSON = {
        'code': 400,
        'body': {'message': 'Bad request, bad JSON.'}
    }

    GenericError = {
        'code': 401
    }

    NotFound = {
        'code': 404
    }

    GeneralConnectionError = {
        'code': 500,
        'body': {'message': 'Something went beep boop and we\'re here now. Sorry for that.'}
    }

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class HttpException(Error):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, errorType, expression='', message=''):
        self.errorType = errorType
        self.expression = expression
        self.message = message

    def GetResponse(self):
        if self.errorType.name == 'GenericError' or self.errorType.name == 'NotFound':
            return json.dumps({'function': self.expression, 'message': self.message}), self.errorType.value['code'], {'ContentType':'application/json'}
        else:
            return json.dumps(self.errorType.value['body']), self.errorType.value['code'], {'ContentType':'application/json'}