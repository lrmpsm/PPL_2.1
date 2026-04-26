import json
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any


from src.utils import (
    optional_param_names,
    required_param_names,
)

from src.models.task import Task
from src.sources.repository import register_source


def parse_json_file(line: str, path: str, line_no: int) -> dict[str, Any]:
    """
    Извлекает из json-файла задачу.
    """
    try:
        task_data = json.loads(line)

        required = set(required_param_names(Task.__init__))
        optional = set(optional_param_names(Task.__init__))
        provided = set(task_data)

        no_extra_attributes_flag = provided <= (required | optional)
        necessary_attributes_flag = required <= provided

        if not (no_extra_attributes_flag and necessary_attributes_flag):
            raise ValueError(f"Invalid attributes in JSON at {path}:{line_no}")

        return task_data

    except json.JSONDecodeError as error:
        raise ValueError(f"Bad JSON at {path}:{line_no}: {error}") from error


@dataclass(frozen=True)
class JsonlSource:
    path: Path
    name: str = "file-jsonl"

    def fetch(self) -> Iterable[Task]:
        '''
        Считывает jsonl-файл, из каждой строки файла берет необходимые данные задачи.
        '''
        with self.path.open("r", encoding="utf-8") as file:
            for line_no, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue
                task_data = parse_json_file(line, str(self.path), line_no)
                yield Task(**task_data)


@register_source("file-jsonl")
def create_json_source(path: Path) -> JsonlSource:
    return JsonlSource(path=path)
