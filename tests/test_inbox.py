from src.contracts.task_source import TaskSource
from src.models.task_status import TaskStatus
from src.sources.generator import GeneratorSource, create_generator_source
from src.constants import (
    TASK_PRIORITY_MAX_VALUE,
    TASK_PRIORITY_MIN_VALUE
)

def test_generator_source_generates_tasks() -> None:
    source = GeneratorSource(count=2)

    tasks = list(source.fetch())

    assert len(tasks) == 2

    assert tasks[0].id == "generator:1"
    assert tasks[1].id == "generator:2"

    for task in tasks:
        assert isinstance(task.description, str)  # для mypy
        assert task.description.strip() != ""
        assert isinstance(task.priority, int)  # для mypy
        assert  TASK_PRIORITY_MIN_VALUE <= task.priority <= TASK_PRIORITY_MAX_VALUE
        assert isinstance(task.status, TaskStatus)


def test_create_generator_source() -> None:
    source = create_generator_source(count=3)

    assert isinstance(source, GeneratorSource)
    assert source.count == 3


def test_generator_source_compiles_with_contract() -> None:
    source = create_generator_source()

    assert isinstance(source, TaskSource)
