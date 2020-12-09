import string
from .HttpException import HttpException, HttpErrorType

charset_standard = string.ascii_letters + string.digits + string.punctuation
charset_standard_with_space = charset_standard + ' '
charset_lowercase = string.ascii_lowercase
charset_uppercase = string.ascii_uppercase
charset_digits = string.digits
charset_lower_and_uppercase = string.ascii_letters

class UserInputRuleSet():
    def __init__(self, rules):
        self.ruleSet = rules

    def getFromRulesByPropertyName(self, propertyName):
        for rule in self.ruleSet:
            if rule.property == propertyName:
                return rule
        return None

    def validateFromPropertyNames(self, propertyNames, JSONValues):
        for propertyName in propertyNames:
            propertyRule = self.getFromRulesByPropertyName(propertyName)
            if propertyRule:
                propertyRule.validate(JSONValues[propertyName])

class UserInputRule():
    def __init__(self, p_property, **rules):
        self.property = p_property
        self.rulesDict = rules

    def validate(self, property_value):
        if not isinstance(property_value, str):
            property_value = str(property_value)

        if 'max_length' in self.rulesDict:
            if len(property_value) > self.rulesDict['max_length']:
                raise HttpException(HttpErrorType.GenericError, 'Input Validation', 'Value of property {} would be truncated.'.format(self.property))

        if 'min_length' in self.rulesDict:
            if len(property_value) < self.rulesDict['min_length']:
                raise HttpException(HttpErrorType.GenericError, 'Input Validation', 'Value of property {} does not meet the minimal length requirement.'.format(self.property))
        
        if 'charset' in self.rulesDict:
            for char in property_value:
                if char not in self.rulesDict['charset']:
                    raise HttpException(HttpErrorType.GenericError, 'Input Validation', 'Value of property {} does not meet the allowed charset.'.format(self.property))