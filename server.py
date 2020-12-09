from flask import Flask, request
from business import Users, Folders, Tasks, ServerSettings
# import logging
# logging.basicConfig(filename='error.log')

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/api/users/create', methods=['POST'])
def apiCreateUser():
    return Users.Create(request)

@app.route('/api/users/login', methods=['POST'])
def apiLogin():
    return Users.Login(request, app.logger)

@app.route('/api/users/logout', methods=['POST'])
def apiLogout():
    return Users.Logout(request)

@app.route('/api/folders/create', methods=['POST'])
def apiFolderCreate():
    return Folders.Create(request)

@app.route('/api/folders/getAll', methods=['POST'])
def apiFolderGetAll():
    return Folders.GetAll(request)

@app.route('/api/tasks/create', methods=['POST'])
def apiTaskCreate():
    return Tasks.Create(request)

@app.route('/api/tasks/getAllByFolderId', methods=['POST'])
def apiTaskGetAllByFolderId():
    return Tasks.GetByFolderId(request)

@app.route('/api/tasks/completeById', methods=['POST'])
def apiTaskCompleteById():
    return Tasks.CompleteTaskById(request)

@app.route('/api/settings/getPublicSetting', methods=['POST'])
def getPublicSetting():
    return ServerSettings.GetPublicSetting(request)

if __name__ == '__main__':
    app.run(port='5000')