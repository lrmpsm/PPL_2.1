import sys
from collections.abc import Iterable
from dataclasses import dataclass
from typing import TextIO

from src.utils import (
    optional_param_names,
    required_param_names,
    param_names,
    is_integer,
)
from src.models.task import Task
from typing import Any
from src.sources.repository import register_source


def extract_task(line: str, line_no: int) -> dict[str, Any]:
    """
    Извлекает из stream данные задачи, разделяя строку по ':'.
    """

    keys = [str(i) for i in param_names(Task.__init__)]
    values = []
    for value in line.split(":"):
        if is_integer(value):
            new_value = int(value)
        values.append(new_value)

    required = required_param_names(Task.__init__)
    optional = optional_param_names(Task.__init__)

    if not (len(required) <= len(values) <= len(required) + len(optional)):
        raise ValueError(
            f"Line: {line_no}. Task must contain id, description, priority and status (optional) separated by ':'."
        )

    task_data = {keys[i]: values[i] for i in range(min(len(keys), len(values)))}
    return task_data



@dataclass(frozen=True)
class StdinLineSource:
    stream: TextIO = sys.stdin
    name: str = "stdin"

    def fetch(self) -> Iterable[Task]:
        for line_no, line in enumerate(self.stream, start=1):
            line = line.strip()
            if not line:
                continue
            task_data = extract_task(line, line_no)
            yield Task(**task_data)


@register_source("stdin")
def create_source() -> StdinLineSource:
    return StdinLineSource()
