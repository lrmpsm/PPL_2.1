class TaskError(Exception):
    """
    Базовое исключение для класса `Task`.
    """

class InvalidTaskIdError(TaskError):
    pass

class InvalidTaskDescriptionError(TaskError):
    pass

class InvalidTaskPriorityError(TaskError):
    pass

class InvalidTaskStatusError(TaskError):
    pass
