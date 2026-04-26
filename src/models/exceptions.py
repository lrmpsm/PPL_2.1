class TaskError(Exception):
    """
    Base exception for task model errors.
    """

class InvalidTaskIdError(TaskError):
    pass

class InvalidTaskDescriptionError(TaskError):
    pass

class InvalidTaskPriorityError(TaskError):
    pass

class InvalidTaskStatusError(TaskError):
    pass
