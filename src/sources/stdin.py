import sys
from collections.abc import Iterable
from dataclasses import dataclass
from typing import TextIO

from src.models.task import Task
from src.sources.repository import register_source


def extract_task(line: str, line_no: int) -> tuple[str, str]:
    """
    Извлекает из stream задачу.
    """
    try:
        task_id, task_payload = line.split(":", maxsplit=1)

        return (task_id, task_payload)
    except ValueError:
        raise ValueError(
            f"Line: {line_no}. Task must contain id and payload, separated by ':' "
        )


@dataclass(frozen=True)
class StdinLineSource:
    stream: TextIO = sys.stdin
    name: str = "stdin"

    def fetch(self) -> Iterable[Task]:
        for line_no, line in enumerate(self.stream, start=1):
            line = line.strip()
            if not line:
                continue
            task_id, task_payload = extract_task(line, line_no)
            yield Task(
                id=task_id,
                payload=task_payload
            )


@register_source("stdin")
def create_source() -> StdinLineSource:
    return StdinLineSource()
