from . import Base
from sqlalchemy import Column, Integer, String, SMALLINT
from utility import UserInput
import json
from enum import Enum

InputRuleSet = UserInput.UserInputRuleSet([
    UserInput.UserInputRule('alias', min_length=1, max_length=20, charset=UserInput.charset_lower_and_uppercase),
    UserInput.UserInputRule('motd', max_length=200, charset=UserInput.charset_standard_with_space)
])

class ValueType(Enum):
    STRING = "string"
    INTEGER = "integer"
    DICTIONARY = "dictionary"
    ARRAY = "list"

class ServerSetting(Base):
    __tablename__ = 'server_settings'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    value = Column(String(500))
    valueType = Column(String(30))
    isPublic = Column(SMALLINT, server_default="0")

    def toJSONObject(self):
        return {
            'id': self.id,
            'name': self.name,
            'value': self.getValue(),
            'valueType': self.valueType,
            'isPublic': bool(self.isPublic)
        }

    def setValue(self, newValue, valueType):
        """
        When passing a dictionary in - do not use single quotes for indexes.
        """
        self.value = str(newValue)
        self.valueType = valueType.value

    def getValue(self):
        if self.valueType == ValueType.STRING.value:
            return self.__getValueString()
        elif self.valueType == ValueType.INTEGER.value:
            return self.__getValueInt()
        elif self.valueType == ValueType.DICTIONARY.value:
            return self.__getValueDict()
        elif self.valueType == ValueType.ARRAY.value:
            return self.__getValueList()

    def __getValueString(self):
        return self.value
    
    def __getValueInt(self):
        return int(self.value)

    def __getValueDict(self):
        return json.loads(self.value)

    def __getValueList(self):
        return list(
            map(
                lambda x: x.strip(), 
                self.value.replace('[', '').replace(']', '').split(',')
            )
        )

def getByName(session, settingName):
    return session.query(ServerSetting).filter_by(name=settingName)