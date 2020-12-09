import xml.etree.ElementTree as ET

def _xmlItemsToDictionary(root):
    toReturn = {}
    for item in root:
        toReturn[item.tag] = item.text
    return toReturn

def _load(configFilename):
    tree = ET.parse(configFilename)
    return tree

def Get(configFilename):
    try:
        conf = _xmlItemsToDictionary(_load(configFilename).getroot())
        return conf
    except:
        return None

def Set(configFilename, **tags):
    tree = _load(configFilename)
    allowedTags = ['databaseServer', 'databaseUser', 'databasePassword', 'databaseName']
    
    for tag in tags:
        if tag in allowedTags:
            tree.find(tag).text = tags[tag]
    
    tree.write(configFilename)