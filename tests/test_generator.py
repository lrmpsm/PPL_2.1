from src.models.task import Task
from src.sources.generator import GeneratorSource


def test_generator_source_creates_requested_count_of_tasks() -> None:
    source = GeneratorSource(count=3)

    tasks = list(source.fetch())

    assert len(tasks) == 3


def test_generator_source_creates_task_objects() -> None:
    source = GeneratorSource(count=2)

    tasks = list(source.fetch())

    assert all(isinstance(task, Task) for task in tasks)


def test_generator_source_generates_expected_ids() -> None:
    source = GeneratorSource(count=3)

    tasks = list(source.fetch())

    assert [task.id for task in tasks] == [
        "generator:1",
        "generator:2",
        "generator:3",
    ]


def test_generator_source_generates_valid_descriptions() -> None:
    source = GeneratorSource(count=3)

    tasks = list(source.fetch())

    for task in tasks:
        assert isinstance(task.description, str)
        assert task.description.strip() != ""
