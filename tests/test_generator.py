from src.models.task import Task
from src.sources.generator import GeneratorSource, create_generator_source
from src.contracts.task_source import TaskSource

def test_generator_source_returns_correct_tasks() -> None:
    source = GeneratorSource(count=3)

    tasks = list(source.fetch())

    assert len(tasks) == 3
    assert [task.id for task in tasks] == [
        "generator:1",
        "generator:2",
        "generator:3",
    ]
    assert all(isinstance(task, Task) for task in tasks)
    assert all(isinstance(task.payload, str) and task.payload for task in tasks)


def test_number_create_generator_source() -> None:
    source = create_generator_source(count=2)

    tasks = list(source.fetch())

    assert len(tasks) == 2


def test_generator_source_compiles_with_contract() -> None:
    source = create_generator_source(count=3)

    assert isinstance(source, TaskSource)
