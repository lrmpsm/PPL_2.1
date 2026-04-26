from pathlib import Path
import logging

import typer
from typer import Typer

from src.inbox.core import InboxApp
from src.sources.repository import REGISTRY
from src.contracts.task_source import TaskSource

cli = Typer(no_args_is_help=True)

logger = logging.getLogger(__name__)

@cli.command("plugins")
def plugins_list() -> None:
    logger.info("Plugins list requested")
    typer.echo("Available plugins:")
    for name in sorted(REGISTRY):
        typer.echo(name)


def _build_sources(
        stdin: bool,
        jsonl: list[Path],
        generator_count: int | None
) -> list[TaskSource]:
    sources: list[TaskSource] = []
    if stdin:
        sources.append(REGISTRY["stdin"]())

        logger.info("Source 'stdin' built")
    for path in jsonl:
        sources.append(REGISTRY["file-jsonl"](path))

        logger.info(f"Source 'file-jsonl' with path '{path}' built")
    if generator_count and generator_count > 0:
        sources.append(REGISTRY["generator"](count=generator_count))

        logger.info(f"Source 'generator' with {generator_count} tasks built")

    return sources


@cli.command("read")
def read(
    stdin: bool = typer.Option(
        False,
        "--stdin",
        help="Read tasks from stdin"),
    jsonl: list[Path] = typer.Option(
        help="Read tasks from jsonl",
        default_factory=list,
        exists=True,
        dir_okay=False,
        readable=True,
    ),
    generator: int | None = typer.Option(
        None,
        "--generator",
        help="Count of generated tasks"
    ),
) -> None:

    logger.info("Read command started")

    raw_sources = _build_sources(stdin, jsonl, generator)

    if not raw_sources:
        logger.warning("No task sources selected")
        typer.echo("No task sources selected")
        typer.echo("\nTotal: 0")
        return

    inbox = InboxApp(raw_sources)
    numbers = 0

    for task in inbox.iter_tasks():
        numbers += 1
        typer.echo(f"[{task.id}] {task.payload}")

        logger.debug(f"Task fetched: id = '{task.id}'")

    logger.info(f"Read command completed: total = {numbers}")

    typer.echo(f"\nTotal: {numbers}")
