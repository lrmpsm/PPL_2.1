from enum import Enum

class TaskStatus(Enum):
    CREATED = "created"
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    FAILED = "failed"
    DONE = "done"
