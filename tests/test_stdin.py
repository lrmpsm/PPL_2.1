import io

import pytest

from src.models.task import Task
from src.sources.stdin import StdinLineSource, create_source, extract_task
from src.contracts.task_source import TaskSource

def test_extract_task_success() -> None:
    task_id, payload = extract_task("abc:hello", 1)

    assert task_id == "abc"
    assert payload == "hello"


def test_extract_task_value_error() -> None:
    with pytest.raises(ValueError):
        extract_task("incorrect_task_format", 3)


def test_stdin_source_skips_empty_lines() -> None:
    fake_input = io.StringIO("\nfirst:первая задача\n\nsecond:вторая задача\n")
    source = StdinLineSource(stream=fake_input)

    tasks = list(source.fetch())

    assert tasks == [
        Task(id="first", payload="первая задача"),
        Task(id="second", payload="вторая задача"),
    ]


def test_stdin_source_compiles_with_contract() -> None:
    source = create_source()

    assert isinstance(source, TaskSource)
