import pytest

from src.inbox.core import InboxApp
from src.models.task import Task


class CorrectSource1:
    name = "1"

    def fetch(self):
        return [Task(id="1", payload="a"), Task(id="2", payload="b")]


class CorrectSource2:
    name = "2"

    def fetch(self):
        return [Task(id="3", payload="c")]


class InvalidSource:
    name = "invalid"


def test_inbox_extracts_all_tasks() -> None:
    app = InboxApp([CorrectSource1(), CorrectSource2()])

    tasks = list(app.iter_tasks())

    assert tasks == [
        Task(id="1", payload="a"),
        Task(id="2", payload="b"),
        Task(id="3", payload="c"),
    ]


def test_inbox_app_rejects_object_that_not_match_protocol() -> None:
    app = InboxApp([InvalidSource()])  # type: ignore

    with pytest.raises(TypeError, match="TaskSource"):
        list(app.iter_tasks())


def test_inbox_no_sources() -> None:
    app = InboxApp()

    assert list(app.iter_tasks()) == []
