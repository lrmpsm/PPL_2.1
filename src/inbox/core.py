from collections.abc import Sequence, Iterable
import logging
from src.models.task import Task
from src.contracts.task_source import TaskSource

logger = logging.getLogger(__name__)

class InboxApp:
    """
    Собирает задачи со всех указанных источников задачи
    Совершает runtime-проверки соблюдения контракта реализованными
    источниками задач.
    """
    def __init__(self, sources: Sequence[TaskSource] | None = None) -> None:
        self._sources = sources if sources is not None else []

    def iter_tasks(self) -> Iterable[Task]:
        for src in self._sources:
            if not isinstance(src, TaskSource):
                logger.error(f"Invalid source object '{src.__repr__}'")
                raise TypeError("Source object must be TaskSource")
            for task in src.fetch():
                yield task
