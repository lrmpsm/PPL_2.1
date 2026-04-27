from collections.abc import Iterable, Iterator
from src.models.task import Task
from src.models.task_status import TaskStatus
from src.models.exceptions import InvalidTaskStatusError


class TaskQueue:
    def __init__(self, tasks: Iterable[Task] | None = None) -> None:
        if tasks is None:
            _tasks = []
        else:
            _tasks = list(tasks)

        self._tasks: list[Task] = _tasks

    def __iter__(self) -> Iterator[Task]:
        return iter(self._tasks)

    def filter_by_status(self, statuses: Iterable[str | TaskStatus]) -> Iterator[Task]:
        normalized_statuses: set[TaskStatus] = set()

        for value in statuses:
            if isinstance(value, str):
                try:
                    value = TaskStatus(value)
                except ValueError:
                    raise InvalidTaskStatusError(f"Invalid task status: {value}")
            normalized_statuses.add(value)

        # return, а не yield, чтобы валидация statuses выполнялась до начала прохода по генератору
        return (
            task
            for task in self
            if task.status in normalized_statuses
        )

    def filter_by_priority_range(self, min_value: int | None = None, max_value: int | None = None) -> Iterator[Task]:
        for task in self:
            if (min_value is None or (type(task.priority) is int and min_value <= task.priority) and
            (max_value is None or (type(task.priority) is int and task.priority <= max_value))):
                yield task

    def filter_by_priority(self, value: int) -> Iterator[Task]:
        for task in self:
            if task.priority == value:
                yield task
