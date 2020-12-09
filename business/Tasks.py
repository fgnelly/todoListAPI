from data import Task, Folder
from utility import SessionHandler
from utility.HttpException import HttpException, HttpErrorType, assertJSON

def Create(request):
    """
    @params: logintoken, name, description, parent_folder_id
    """
    requestJSON = request.get_json(silent=True)
    try:
        assertJSON(requestJSON, ['logintoken', 'name', 'description', 'parent_folder_id'])
        Task.InputRuleSet.validateFromPropertyNames(['name', 'description'], requestJSON)

        with SessionHandler.app_and_db_session_scope(requestJSON['logintoken'], SessionHandler.PermissionLevel.USER) as session:
            if Folder.checkIfFolderExists(session.db_session, requestJSON['parent_folder_id'], session.current_user.id) < 1:
                raise HttpException(HttpErrorType.NotFound, 'Task Create', 'No such folder found under current user')

            addedTask = Task.addNew(session.db_session, session.current_user.id, requestJSON['name'], requestJSON['description'], requestJSON['parent_folder_id'])
            return SessionHandler.returnRequestOK(addedTask.toJSONObject())

    except HttpException as exc:
        return exc.GetResponse()

def GetByFolderId(request):
    """
    @params: logintoken, parent_folder_id
    """
    requestJSON = request.get_json(silent=True)
    try:
        assertJSON(requestJSON, ['logintoken', 'parent_folder_id'])

        with SessionHandler.app_and_db_session_scope(requestJSON['logintoken'], SessionHandler.PermissionLevel.USER) as session:
            foundTasks = Task.getAllFromFolderId(session.db_session, requestJSON['parent_folder_id'], session.current_user.id)
            JSONTasks = [] if foundTasks.count() == 0 else list(map(lambda x: x.toJSONObject(), foundTasks))
            return SessionHandler.returnRequestOK({"tasks": JSONTasks})

    except HttpException as exc:
        return exc.GetResponse()

def CompleteTaskById(request):
    """
    @params: logintoken, task_id
    """
    requestJSON = request.get_json(silent=True)
    try:
        assertJSON(requestJSON, ['logintoken', 'task_id'])

        with SessionHandler.app_and_db_session_scope(requestJSON['logintoken'], SessionHandler.PermissionLevel.USER) as session:
            foundTask = Task.getById(session.db_session, session.current_user.id, requestJSON['task_id'])
            if foundTask.count() == 0:
                raise HttpException(HttpErrorType.NotFound, 'Updating Task', 'No task found for given id.')

            foundTask.first().setAsCompleted()
            return SessionHandler.returnRequestOK()

    except HttpException as exc:
        return exc.GetResponse()