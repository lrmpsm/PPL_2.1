import pytest

from src.contracts.task_source import TaskSource
from src.models.task_status import TaskStatus
from src.sources.json import JsonlSource, create_json_source, parse_json_file


def test_parse_task_success() -> None:
    result = parse_json_file(
        '{"id": "1", "description": "hello", "priority": 3, "status": "created"}',
        "tasks.jsonl",
        1,
    )

    assert result == {
        "id": "1",
        "description": "hello",
        "priority": 3,
        "status": "created",
    }


def test_jsonl_source_reads(tmp_path) -> None:
    path = tmp_path / "tasks.jsonl"
    path.write_text(
        "\n"
        '{"id": "1", "description": "hello", "priority": 3, "status": "created"}\n'
        "\n"
        '{"id": "2", "description": "world", "priority": 5, "status": "pending"}\n',
        encoding="utf-8",
    )

    source = JsonlSource(path=path)
    tasks = list(source.fetch())

    assert len(tasks) == 2

    assert tasks[0].id == "1"
    assert tasks[0].description == "hello"
    assert tasks[0].priority == 3
    assert tasks[0].status == TaskStatus.CREATED

    assert tasks[1].id == "2"
    assert tasks[1].description == "world"
    assert tasks[1].priority == 5
    assert tasks[1].status == TaskStatus.PENDING


def test_parse_task_value_error() -> None:
    with pytest.raises(ValueError, match="Bad JSON"):
        parse_json_file('{"id": 1', "tasks.jsonl", 2)


def test_json_source_compiles_with_contract(tmp_path) -> None:
    path = tmp_path / "tasks.jsonl"
    path.write_text(
        '{"id": "1", "description": "hello", "priority": 3, "status": "created"}\n',
        encoding="utf-8",
    )

    source = create_json_source(path)

    assert isinstance(source, TaskSource)
