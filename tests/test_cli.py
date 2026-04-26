from typer.testing import CliRunner

from src.cli import _build_sources, cli
runner = CliRunner()


def test_plugins_command() -> None:
    result = runner.invoke(cli, ["plugins"])

    assert result.exit_code == 0
    assert "Available plugins:" in result.output
    assert "file-jsonl" in result.output
    assert "generator" in result.output
    assert "stdin" in result.output


def test_build_sources_creates_requested_source_objects(tmp_path) -> None:
    path = tmp_path / "tasks.jsonl"
    path.write_text('some kind task\n', encoding="utf-8")

    sources = _build_sources(stdin=True, jsonl=[path], generator_count=2)

    assert len(sources) == 3
    assert [source.name for source in sources] == ["stdin", "file-jsonl", "generator"]


def test_read_command_no_sources(monkeypatch) -> None:
    monkeypatch.setattr("src.cli._build_sources", lambda stdin, jsonl, generator: [])

    result = runner.invoke(cli, ["read"])

    assert result.exit_code == 0
    assert "Total: 0" in result.output
