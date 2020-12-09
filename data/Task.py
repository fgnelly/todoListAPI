from . import Base
from sqlalchemy import Column, Integer, String, SMALLINT
from utility import UserInput

InputRuleSet = UserInput.UserInputRuleSet([
    UserInput.UserInputRule('name', min_length=1, max_length=50, charset=UserInput.charset_standard_with_space),
    UserInput.UserInputRule('description', max_length=200, charset=UserInput.charset_standard_with_space)
])

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    owner_userid = Column(Integer)
    name = Column(String(50))
    description = Column(String(200))
    priority = Column(Integer)
    parent_folder_id = Column(Integer)
    isCompleted = Column(SMALLINT, server_default="0")

    def toJSONObject(self):
        return {
            'id': self.id,
            'owner_userid': self.owner_userid,
            'parent_folder_id': self.parent_folder_id,
            'name': self.name,
            'description': self.description,
            'priority': self.priority,
            'isCompleted': self.isCompleted
        }

    def setAsCompleted(self):
        self.isCompleted = 1

def getAllFromFolderId(session, parent_folder_id, owner_id):
    return session.query(Task).filter_by(owner_userid=owner_id, parent_folder_id=parent_folder_id)

def getById(session, owner_id, task_id):
    return session.query(Task).filter_by(owner_userid=owner_id, id=task_id)

def addNew(session, ownerid, name, description, folder_id):
    allFromUserCount = getAllFromFolderId(session, folder_id, ownerid).count()
    db_task = Task(owner_userid=ownerid, name=name, description=description, priority=allFromUserCount, parent_folder_id=folder_id)
    session.add(db_task)
    return db_task