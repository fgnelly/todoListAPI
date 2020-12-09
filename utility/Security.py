from bcrypt import hashpw, gensalt, checkpw
from secrets import token_urlsafe
import time

def timestampNow():
    return int(round(time.time() * 1000))

def getTokenValidityTime():
    oneDayInMS = 1000 * 60 * 60 * 24
    return timestampNow() + oneDayInMS

def encryptPassword(password):
    if len(password) > 56:
        password = password[0:57]
    return hashpw(password.encode(), gensalt())

def verifyPassword(password, passwordHash):
    if len(password) > 56:
        password = password[0:57]
    return checkpw(password.encode(), passwordHash.encode())

def generateSafeRandomToken():
    return token_urlsafe(128)