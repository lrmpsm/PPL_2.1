import io

import pytest

from src.contracts.task_source import TaskSource
from src.models.task_status import TaskStatus
from src.sources.stdin import StdinLineSource, create_source, extract_task


def test_extract_task_success() -> None:
    task_data = extract_task("abc:hello:3:created", 1)

    assert task_data == {
        "id": "abc",
        "description": "hello",
        "priority": 3,
        "status": "created",
    }


def test_extract_task_value_error() -> None:
    with pytest.raises(ValueError):
        extract_task("incorrect_task_format", 3)


def test_stdin_source_skips_empty_lines() -> None:
    fake_input = io.StringIO(
        "\n"
        "first:первая задача:3:created\n"
        "\n"
        "second:вторая задача:5:pending\n"
    )
    source = StdinLineSource(stream=fake_input)

    tasks = list(source.fetch())

    assert len(tasks) == 2

    assert tasks[0].id == "first"
    assert tasks[0].description == "первая задача"
    assert tasks[0].priority == 3
    assert tasks[0].status == TaskStatus.CREATED

    assert tasks[1].id == "second"
    assert tasks[1].description == "вторая задача"
    assert tasks[1].priority == 5
    assert tasks[1].status == TaskStatus.PENDING


def test_stdin_source_compiles_with_contract() -> None:
    source = create_source()

    assert isinstance(source, TaskSource)
