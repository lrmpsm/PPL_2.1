import pytest

from src.models.task import Task
from src.sources.json import JsonlSource, create_json_source, parse_json_file
from src.contracts.task_source import TaskSource

def test_parse_task_success() -> None:
    result = parse_json_file(
        '{"id": "1", "payload": "hello"}',
        "tasks.jsonl",
        1,
    )

    assert result == {"id": "1", "payload": "hello"}


def test_jsonl_source_reads(tmp_path) -> None:
    path = tmp_path / "tasks.jsonl"
    path.write_text(
        '\n{"id": "1", "payload": "hello"}\n\n{"id": "2", "payload": {"n": 10}}\n',
        encoding="utf-8",
    )

    source = JsonlSource(path=path)
    tasks = list(source.fetch())

    assert tasks == [
        Task(id="1", payload="hello"),
        Task(id="2", payload={"n": 10}),
    ]


def test_parse_task_value_error() -> None:
    with pytest.raises(ValueError, match="Bad JSON"):
        parse_json_file('{"id": 1', "tasks.jsonl", 2)


def test_json_source_compiles_with_contract(tmp_path) -> None:
    path = tmp_path / "tasks.jsonl"
    path.write_text('{"id": "1", "payload": "x"}\n', encoding="utf-8")

    source = create_json_source(path)

    assert isinstance(source, TaskSource)
