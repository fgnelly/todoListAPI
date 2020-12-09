from . import Base, engine
from sqlalchemy import Column, Integer, String, BIGINT, SMALLINT
from utility import Security

class AppSession(Base):
    __tablename__ = 'loginsessions'

    id = Column(Integer, primary_key=True, nullable=False)
    userid = Column(Integer, nullable=False)
    token = Column(String(171, collation='utf8mb4_bin'), nullable=False)
    validUntil = Column(BIGINT, nullable=False)
    lastUsed = Column(BIGINT, nullable=False, server_default="0")
    isInvalidated = Column(SMALLINT, server_default="0", nullable=False)
    permissionLevel = Column(Integer, nullable=False, server_default="1") #0 - none, 1 - user, 2 - admin
    userAgent = Column(String(128))

    def invalidate(self):
        self.isInvalidated = 1

    def updateLastUsed(self):
        self.lastUsed = Security.timestampNow()

def tokenAlreadyExists(session, token):
    return session.query(AppSession).filter_by(token=token).count() > 0

def addNew(session, userid, permissionLevel, userAgent=""):
    randomSessionToken = Security.generateSafeRandomToken()
    while tokenAlreadyExists(session, randomSessionToken):
        randomSessionToken = Security.generateSafeRandomToken()
    
    db_session = AppSession(userid=userid, token=randomSessionToken, validUntil=Security.getTokenValidityTime(), userAgent=userAgent)
    session.add(db_session)
    return db_session

def getAllValidFromUserId(session, userid):
    allSessions = session.query(AppSession).filter_by(isInvalidated=0, userid=userid)
    for userSession in allSessions:
        if(checkIfSessionValid(userSession)):
            return userSession
    else:
        return None

def addNewOrReturnLastIfValid(session, userid, permissionLevel, userAgent=""):
    validSessionForUser = getAllValidFromUserId(session, userid)
    return validSessionForUser if validSessionForUser else addNew(session, userid, permissionLevel, userAgent)

def checkIfSessionValid(app_session):
    return app_session.validUntil > Security.timestampNow() and app_session.isInvalidated == False

def loadValidFromToken(session, token):
    foundAppSession = session.query(AppSession).filter_by(token=token)
    return foundAppSession.first() if foundAppSession.count() == 1 and checkIfSessionValid(foundAppSession.first()) else None