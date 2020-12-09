from . import Base
from sqlalchemy import Column, Integer, String
from utility import UserInput

InputRuleSet = UserInput.UserInputRuleSet([
    UserInput.UserInputRule('name', min_length=1, max_length=50, charset=UserInput.charset_standard),
    UserInput.UserInputRule('description', max_length=200, charset=UserInput.charset_standard_with_space)
])

class Folder(Base):
    __tablename__ = 'folders'

    id = Column(Integer, primary_key=True)
    owner_userid = Column(Integer)
    name = Column(String(50))
    description = Column(String(200))
    priority = Column(Integer)

    def toJSONObject(self):
        return {
            'id': self.id,
            'owner_userid': self.owner_userid,
            'name': self.name,
            'description': self.description,
            'priority': self.priority
        }

    def rename(self, newName):
        self.name = newName

    def reprioritize(self, newPriority):
        self.priority = newPriority

    def updateDescription(self, newDesc):
        self.description = newDesc

def getAllFromOwnerId(session, ownerid):
    return session.query(Folder).filter_by(owner_userid=ownerid)

def addNew(session, ownerid, name, description):
    allFromUserCount = getAllFromOwnerId(session, ownerid).count()
    db_folder = Folder(owner_userid=ownerid, name=name, description=description, priority=allFromUserCount)
    session.add(db_folder)
    return db_folder

def checkIfFolderExists(session, folder_id, ownerid):
    return session.query(Folder).filter_by(owner_userid=ownerid, id=folder_id).count()