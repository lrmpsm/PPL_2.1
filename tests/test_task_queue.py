from collections.abc import Iterable, Iterator

import pytest

from src.models.exceptions import InvalidTaskStatusError
from src.models.task import Task
from src.models.task_queue import TaskQueue
from src.models.task_status import TaskStatus
from src.constants import (
    TASK_PRIORITY_DEFAULT_VALUE,
    TASK_PRIORITY_MAX_VALUE,
    TASK_PRIORITY_MIN_VALUE,
)

class FakeTaskSource:
    """
    Класс для имитации источника задач.
    """
    name = "list-source"

    def __init__(self, tasks: Iterable[Task]) -> None:
        self._tasks = list(tasks)
        self.fetch_calls = 0

    def fetch(self) -> Iterator[Task]:
        self.fetch_calls += 1
        return iter(self._tasks)


def make_task(
    id: str,
    priority: int = 3,
    status: TaskStatus = TaskStatus.CREATED,
) -> Task:
    return Task(
        id=id,
        description=f"description for task with id = {id}",
        priority=priority,
        status=status,
    )


def task_ids(tasks: Iterable[Task]) -> list[str]:
    return [str(task.id) for task in tasks]


def test_queue_iterates_all_sources_order() -> None:
    first = make_task("first", priority=1)
    second = make_task("second", priority=2)
    third = make_task("third", priority=3)

    queue = TaskQueue([
        FakeTaskSource([first, second]),
        FakeTaskSource([third]),
    ])

    assert list(queue) == [first, second, third]


def test_queue_repeated_iteration() -> None:
    source = FakeTaskSource([
        make_task("first"),
        make_task("second"),
    ])
    queue = TaskQueue(source)

    assert task_ids(queue) == ["first", "second"]
    assert task_ids(queue) == ["first", "second"]
    assert source.fetch_calls == 2


def test_queue_iterator_stop_iteration_when_empty() -> None:
    task = make_task("only")
    queue = TaskQueue([FakeTaskSource([task])])

    iterator = iter(queue)

    assert next(iterator) is task
    with pytest.raises(StopIteration):
        next(iterator)


def test_filter_by_statuses_accepts_enum_and_string_statuses() -> None:
    created = make_task("created", status=TaskStatus.CREATED)
    pending = make_task("pending", status=TaskStatus.PENDING)
    done = make_task("done", status=TaskStatus.DONE)
    queue = TaskQueue([FakeTaskSource([created, pending, done])])

    result = queue.filter_by_statuses(["pending", TaskStatus.DONE])

    assert task_ids(result) == ["pending", "done"]


def test_filter_by_statuses_validates_status_before_fetch() -> None:
    source = FakeTaskSource([make_task("first")])
    queue = TaskQueue([source])

    with pytest.raises(InvalidTaskStatusError):
        queue.filter_by_statuses(["unknown"])

    assert source.fetch_calls == 0


def test_filter_by_priority() -> None:
    queue = TaskQueue([FakeTaskSource([
        make_task("very low", priority=TASK_PRIORITY_MIN_VALUE),
        make_task("middle1", priority=TASK_PRIORITY_DEFAULT_VALUE),
        make_task("very high", priority=TASK_PRIORITY_MAX_VALUE),
        make_task("middle2", priority=TASK_PRIORITY_DEFAULT_VALUE),
    ])])

    result = queue.filter_by_priority(TASK_PRIORITY_DEFAULT_VALUE)

    assert task_ids(result) == ["middle1", "middle2"]


def test_filter_by_priority_range_two_params() -> None:
    queue = TaskQueue([FakeTaskSource([
        make_task("one", priority=TASK_PRIORITY_MIN_VALUE),
        make_task("three", priority=3),
        make_task("five", priority=5),
    ])])

    result = queue.filter_by_priority_range(min_value=2, max_value=4)

    assert task_ids(result) == ["three"]


def test_filter_by_priority_range_one_param() -> None:
    queue = TaskQueue([FakeTaskSource([
        make_task("one", priority=TASK_PRIORITY_MIN_VALUE),
        make_task("three", priority=TASK_PRIORITY_DEFAULT_VALUE),
        make_task("five", priority=TASK_PRIORITY_MAX_VALUE),
    ])])

    assert task_ids(queue.filter_by_priority_range(min_value=TASK_PRIORITY_DEFAULT_VALUE)) == [
        "three",
        "five",
    ]
    assert task_ids(queue.filter_by_priority_range(max_value=TASK_PRIORITY_DEFAULT_VALUE)) == [
        "one",
        "three",
    ]
    assert task_ids(queue.filter_by_priority_range()) == [
        "one",
        "three",
        "five",
    ]


def test_empty_queue_returns_empty_iterators() -> None:
    queue = TaskQueue([])

    assert list(queue) == []
    assert list(queue.filter_by_statuses([TaskStatus.CREATED])) == []
    assert list(queue.filter_by_priority(3)) == []
    assert list(queue.filter_by_priority_range()) == []
