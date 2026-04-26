from datetime import datetime, timezone
from .descriptors import NonEmptyLimitedString, Priority, TimeAsText
from .task_status import TaskStatus
from .exceptions import (
    InvalidTaskStatusError,
    InvalidTaskIdError,
    InvalidTaskDescriptionError,
)
from src.constants import (
    TASK_DESCRIPTION_MAX_LENGTH,
    TASK_ID_MAX_LENGTH,
    TASK_PRIORITY_MAX_VALUE,
    TASK_PRIORITY_MIN_VALUE,
    TASK_PRIORITY_DEFAULT_VALUE,
)
class Task:
    id = NonEmptyLimitedString(
        max_length=TASK_ID_MAX_LENGTH,
        error_cls=InvalidTaskIdError,
        field_name="Id",
    )
    description = NonEmptyLimitedString(
        max_length=TASK_DESCRIPTION_MAX_LENGTH,
        error_cls=InvalidTaskDescriptionError,
        field_name="Description",
    )
    priority = Priority(
        min_value = TASK_PRIORITY_MIN_VALUE,
        max_value = TASK_PRIORITY_MAX_VALUE,
    )
    created_at_text = TimeAsText("created_at")
    updated_at_text = TimeAsText("updated_at")

    def __init__(
            self,
            id: str,
            description: str,
            priority: int = TASK_PRIORITY_DEFAULT_VALUE,
            status: TaskStatus | str = TaskStatus.CREATED,
    ) -> None:
        self.id = id
        self.description = description
        self.priority = priority
        self.status = status
        now = datetime.now(timezone.utc)
        self._created_at = now
        self._updated_at = now

    def _touch(self) -> None:
        if "_created_at" in self.__dict__:
            self._updated_at = datetime.now(timezone.utc)
            self.__dict__.pop("updated_at_text", None)

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    @property
    def is_ready(self) -> bool:
        return self.status == TaskStatus.PENDING

    @property
    def status(self) -> TaskStatus:
        return self._status

    @status.setter
    def status(self, value: TaskStatus | str) -> None:
        if isinstance(value, str):
            try:
                value = TaskStatus(value)
            except ValueError:
                raise InvalidTaskStatusError(f"Invalid task status: {value}")

        elif not isinstance(value, TaskStatus):
            raise InvalidTaskStatusError(
                "Status must be a TaskStatus object or a valid status string."
            )

        self._status = value
        self._touch()


    def __str__(self) -> str:
        return (
            f"Task(id={self.id},\n"
            f"description={self.description},\n"
            f"priority={self.priority},\n"
            f"status={self.status.value},\n"
            f"created_at_text={self.created_at_text})"
        )
