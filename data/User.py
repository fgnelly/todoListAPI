from . import Base
from sqlalchemy import Column, Integer, String
from utility import UserInput

InputRuleSet = UserInput.UserInputRuleSet([
    UserInput.UserInputRule('name', min_length=3, max_length=50, charset=UserInput.charset_lower_and_uppercase + UserInput.charset_digits + ' '),
    UserInput.UserInputRule('username', min_length=5, max_length=50, charset=UserInput.charset_lower_and_uppercase + UserInput.charset_digits),
    UserInput.UserInputRule('password', min_length=1)
])

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    username = Column(String(50))
    password = Column(String(200))

    def updatePassword(self, newPassword):
        self.password = newPassword

    def toJSONObject(self):
        return {
            'userid': self.id,
            'name': self.name,
            'username': self.username
        }

def getAll(session):
    for instance in session.query(User).order_by(User.id):
        print(instance.name, instance.username)

def loadFromDbByUsername(session, username):
    return session.query(User).filter_by(username=username).first()

def loadFromDbById(session, uid):
    return session.query(User).filter_by(id=uid).first()

def addNew(session, name, username, password):
    db_user = User(name=name, username=username, password=password)
    session.add(db_user)
    return db_user