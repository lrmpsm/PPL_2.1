from datetime import datetime, timezone
from typing import Any
import time
import pytest

from src.constants import (
    TASK_DESCRIPTION_MAX_LENGTH,
    TASK_ID_MAX_LENGTH,
    TASK_PRIORITY_DEFAULT_VALUE,
    TASK_PRIORITY_MIN_VALUE,
    TASK_PRIORITY_MAX_VALUE,
)
from src.models.exceptions import (
    InvalidTaskDescriptionError,
    InvalidTaskIdError,
    InvalidTaskPriorityError,
    InvalidTaskStatusError,
)
from src.models.task import Task
from src.models.task_status import TaskStatus


def make_task_data() -> dict[str, Any]:
    return {
        "id": "task-1",
        "description": "this is the first task",
        "priority": TASK_PRIORITY_MIN_VALUE,
        "status": TaskStatus.PENDING,
    }


# создание задачи с различным набором параметров

def test_create_all_params() -> None:
    task_data = make_task_data()

    task = Task(**task_data)

    assert task.id == "task-1"
    assert task.description == "this is the first task"
    assert task.priority == TASK_PRIORITY_MIN_VALUE
    assert task.status == TaskStatus.PENDING
    assert task.is_ready is True
    assert task.updated_at == task.created_at


def test_create_all_params_but_status_is_str() -> None:
    task_data = make_task_data()
    task_data["status"] = "done"

    task = Task(**task_data)

    assert task.id == "task-1"
    assert task.description == "this is the first task"
    assert task.priority == TASK_PRIORITY_MIN_VALUE
    assert task.status == TaskStatus.DONE
    assert task.is_ready is False
    assert task.updated_at == task.created_at


def test_create_without_status() -> None:
    task_data = make_task_data()
    del task_data["status"]

    task = Task(**task_data)

    assert task.id == "task-1"
    assert task.description == "this is the first task"
    assert task.priority == TASK_PRIORITY_MIN_VALUE
    assert task.status == TaskStatus.CREATED
    assert task.is_ready is False
    assert task.updated_at == task.created_at


def test_create_without_priority() -> None:
    task_data = make_task_data()
    del task_data["priority"]

    task = Task(**task_data)

    assert task.id == "task-1"
    assert task.description == "this is the first task"
    assert task.priority == TASK_PRIORITY_DEFAULT_VALUE
    assert task.status == TaskStatus.PENDING
    assert task.is_ready is True
    assert task.updated_at == task.created_at


# ошибки при создании задачи с невалидным id

def test_create_with_non_string_id_raises_error() -> None:
    task_data = make_task_data()
    task_data["id"] = 1

    with pytest.raises(InvalidTaskIdError):
        Task(**task_data)


def test_create_with_blank_id_raises_error() -> None:
    task_data = make_task_data()
    task_data["id"] = "    \n       "

    with pytest.raises(InvalidTaskIdError):
        Task(**task_data)


def test_create_with_too_long_id_raises_error() -> None:
    task_data = make_task_data()
    task_data["id"] = "1" * (TASK_ID_MAX_LENGTH + 1)

    with pytest.raises(InvalidTaskIdError):
        Task(**task_data)


# ошибки при присвоении задаче невалидного id

def test_set_non_string_id_raises_error() -> None:
    task = Task(**make_task_data())

    with pytest.raises(InvalidTaskIdError):
        setattr(task, "id", 1)


def test_set_blank_id_raises_error() -> None:
    task = Task(**make_task_data())

    with pytest.raises(InvalidTaskIdError):
        task.id = "    \n       "


def test_set_too_long_id_raises_error() -> None:
    task = Task(**make_task_data())

    with pytest.raises(InvalidTaskIdError):
        task.id = "1" * (TASK_ID_MAX_LENGTH + 1)


# ошибки при создании задачи с невалидным description

def test_create_with_non_string_description_raises_error() -> None:
    task_data = make_task_data()
    task_data["description"] = []

    with pytest.raises(InvalidTaskDescriptionError):
        Task(**task_data)


def test_create_with_blank_description_raises_error() -> None:
    task_data = make_task_data()
    task_data["description"] = "   \n       "

    with pytest.raises(InvalidTaskDescriptionError):
        Task(**task_data)


def test_create_with_too_long_description_raises_error() -> None:
    task_data = make_task_data()
    task_data["description"] = "1" * (TASK_DESCRIPTION_MAX_LENGTH + 1)

    with pytest.raises(InvalidTaskDescriptionError):
        Task(**task_data)


# ошибки при присвоении задаче невалидного description

def test_set_non_string_description_raises_error() -> None:
    task = Task(**make_task_data())

    with pytest.raises(InvalidTaskDescriptionError):
        setattr(task, "description", 10)


def test_set_blank_description_raises_error() -> None:
    task = Task(**make_task_data())

    with pytest.raises(InvalidTaskDescriptionError):
        task.description = "   \n   "


def test_set_too_long_description_raises_error() -> None:
    task = Task(**make_task_data())

    with pytest.raises(InvalidTaskDescriptionError):
        task.description = "1" * (TASK_DESCRIPTION_MAX_LENGTH + 1)


# ошибки при создании задачи с невалидным priority

def test_create_with_non_integer_priority_raises_error() -> None:
    task_data = make_task_data()
    task_data["priority"] = "high"

    with pytest.raises(InvalidTaskPriorityError):
        Task(**task_data)


def test_create_with_too_low_priority_raises_error() -> None:
    task_data = make_task_data()
    task_data["priority"] = TASK_PRIORITY_MIN_VALUE - 1

    with pytest.raises(InvalidTaskPriorityError):
        Task(**task_data)


def test_create_with_too_high_priority_raises_error() -> None:
    task_data = make_task_data()
    task_data["priority"] = TASK_PRIORITY_MAX_VALUE + 1

    with pytest.raises(InvalidTaskPriorityError):
        Task(**task_data)


# ошибки при присвоении задаче невалидного priority

def test_set_non_integer_priority_raises_error() -> None:
    task = Task(**make_task_data())

    with pytest.raises(InvalidTaskPriorityError):
        setattr(task, "priority", "high")


def test_set_too_low_priority_raises_error() -> None:
    task = Task(**make_task_data())

    with pytest.raises(InvalidTaskPriorityError):
        task.priority = TASK_PRIORITY_MIN_VALUE - 1


def test_set_too_high_priority_raises_error() -> None:
    task = Task(**make_task_data())

    with pytest.raises(InvalidTaskPriorityError):
        task.priority = TASK_PRIORITY_MAX_VALUE + 1


# ошибки при создании задачи с невалидным status

def test_create_with_unknown_status_string_raises_error() -> None:
    task_data = make_task_data()
    task_data["status"] = "unknown"

    with pytest.raises(InvalidTaskStatusError):
        Task(**task_data)


def test_create_with_invalid_status_type_raises_error() -> None:
    task_data = make_task_data()
    task_data["status"] = 123

    with pytest.raises(InvalidTaskStatusError):
        Task(**task_data)


# ошибки при присвоении задаче невалидного status

def test_set_unknown_status_string_raises_error() -> None:
    task = Task(**make_task_data())

    with pytest.raises(InvalidTaskStatusError):
        task.status = "unknown"


def test_set_invalid_status_type_raises_error() -> None:
    task = Task(**make_task_data())

    with pytest.raises(InvalidTaskStatusError):
        setattr(task, "status", 123)


# обновление полей updated_at и updated_at_text при изменении атрибутов

def test_change_updated_at_while_changing_id() -> None:
    task = Task(**make_task_data())

    _ = task.updated_at_text
    old_updated_at = task.updated_at

    assert "updated_at_text" in task.__dict__
    time.sleep(0.01)
    task.id = "new-id"

    assert old_updated_at < task.updated_at
    assert "updated_at_text" not in task.__dict__

    new_updated_at_text = task.updated_at_text

    assert isinstance(new_updated_at_text, str)
    assert "updated_at_text" in task.__dict__


def test_change_updated_at_while_changing_description() -> None:
    task = Task(**make_task_data())

    _ = task.updated_at_text
    old_updated_at = task.updated_at

    assert "updated_at_text" in task.__dict__
    time.sleep(0.01)
    task.description = "new description"

    assert old_updated_at < task.updated_at
    assert "updated_at_text" not in task.__dict__

    new_updated_at_text = task.updated_at_text

    assert isinstance(new_updated_at_text, str)
    assert "updated_at_text" in task.__dict__


def test_change_updated_at_while_changing_priority() -> None:
    task = Task(**make_task_data())

    _ = task.updated_at_text
    old_updated_at = task.updated_at

    assert "updated_at_text" in task.__dict__
    time.sleep(0.01)
    task.priority = TASK_PRIORITY_MAX_VALUE

    assert old_updated_at < task.updated_at
    assert "updated_at_text" not in task.__dict__

    new_updated_at_text = task.updated_at_text

    assert isinstance(new_updated_at_text, str)
    assert "updated_at_text" in task.__dict__


def test_change_updated_at_while_changing_status() -> None:
    task = Task(**make_task_data())

    _ = task.updated_at_text
    old_updated_at = task.updated_at

    assert "updated_at_text" in task.__dict__

    time.sleep(0.01)
    task.status = "created"

    assert old_updated_at < task.updated_at
    assert "updated_at_text" not in task.__dict__

    new_updated_at_text = task.updated_at_text

    assert isinstance(new_updated_at_text, str)
    assert "updated_at_text" in task.__dict__


# ошибки при попытке изменения read-only properties

def test_set_created_at_raises_attribute_error() -> None:
    task = Task(**make_task_data())

    with pytest.raises(AttributeError):
        setattr(task, "created_at", datetime.now(timezone.utc))


def test_set_updated_at_raises_attribute_error() -> None:
    task = Task(**make_task_data())

    with pytest.raises(AttributeError):
        setattr(task, "updated_at", datetime.now(timezone.utc))


# демонстрация изменения атрибутов с non-data дескрипторами

def test_created_at_text_can_be_overridden_because_it_is_non_data_descriptor() -> None:
    task = Task(**make_task_data())

    task.created_at_text = "custom created_at_text"

    assert task.created_at_text == "custom created_at_text"


def test_updated_at_text_can_be_overridden_because_it_is_non_data_descriptor() -> None:
    task = Task(**make_task_data())

    task.updated_at_text = "custom updated_at_text"

    assert task.updated_at_text == "custom updated_at_text"


def test_updated_at_text_override_is_removed_after_task_change() -> None:
    task = Task(**make_task_data())

    task.updated_at_text = "custom updated_at_text"

    assert task.updated_at_text == "custom updated_at_text"

    task.description = "changed description"

    assert task.updated_at_text != "custom updated_at_text"


# корректное изменение свойства is_ready при изменении status

def test_is_ready_changes_when_status_changes() -> None:
    task = Task(**make_task_data())

    assert task.status == TaskStatus.PENDING
    assert task.is_ready is True

    task.status = TaskStatus.CREATED

    assert task.status == TaskStatus.CREATED
    assert task.is_ready is False

    task.status = "pending"

    assert task.status == TaskStatus.PENDING
    assert task.is_ready is True

    task.status = TaskStatus.DONE

    assert task.status == TaskStatus.DONE
    assert task.is_ready is False


# демонстрация поведения data descriptor

def test_data_descriptor_has_priority_over_instance_dict() -> None:
    task = Task(**make_task_data())

    task.__dict__["priority"] = TASK_PRIORITY_MAX_VALUE + 100

    assert task.priority == TASK_PRIORITY_MIN_VALUE
    assert task.__dict__["priority"] == TASK_PRIORITY_MAX_VALUE + 100
