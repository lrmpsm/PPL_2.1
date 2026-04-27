from collections.abc import Iterable, Iterator
from src.models.task import Task
from src.models.task_status import TaskStatus
from src.models.exceptions import InvalidTaskStatusError
from src.contracts.task_source import TaskSource


class TaskQueue:
    """
    Ленивая очередь задач, объединяющая несколько
    источников в один поток.

    Очередь получает задачи из источников во время
    итерации и не хранит сами задачи в памяти.
    """
    def __init__(self, sources: Iterable[TaskSource] | TaskSource) -> None:
        """
        Создать очередь задач, указав источники задач.
        """
        if isinstance(sources, TaskSource):
            sources = [sources]

        self.sources: list[TaskSource] = list(sources)

    def __iter__(self) -> Iterator[Task]:
        for source in self.sources:
            for task in source.fetch():
                yield task

    def filter_by_statuses(self, statuses: Iterable[str | TaskStatus]) -> Iterator[Task]:
        """
        Отфильтровать задачи из источников по
        принадлежности к списку из статусов
        выполнения задач.

        Перед непосредственной фильтрацией задач
        производится преобразование итерируемого
        объекта `statuses` из Iterable[str | TaskStatus]
        в Iterable[TaskStatus].
        """
        normalized_statuses: set[TaskStatus] = set()

        for value in statuses:
            if isinstance(value, str):
                try:
                    value = TaskStatus(value)
                except ValueError:
                    raise InvalidTaskStatusError(f"Invalid task status: {value}")
            normalized_statuses.add(value)

        # return, а не yield, чтобы валидация statuses выполнялась до начала прохода по генератору
        return(
                task
                for task in self
                if task.status in normalized_statuses
            )


    def filter_by_priority_range(self, min_value: int | None = None, max_value: int | None = None) -> Iterator[Task]:
        """
        Отфильтраовать задачи из источников по
        промежутку возможных приоритетов
        """
        for task in self:
            if ((min_value is None or (type(task.priority) is int and min_value <= task.priority)) and
            (max_value is None or (type(task.priority) is int and task.priority <= max_value))):
                yield task


    def filter_by_priority(self, value: int) -> Iterator[Task]:
        """
        Отфильтровать задачи из источников по
        совпадению с указанным приоритетом.
        """
        for task in self:
            if task.priority == value:
                yield task
