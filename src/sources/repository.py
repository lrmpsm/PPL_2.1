import logging
from typing import Callable, Any
from src.contracts.task_source import TaskSource

SourceFactory = Callable[..., TaskSource]

REGISTRY: dict[str, SourceFactory] = {}

logger = logging.getLogger(__name__)

def register_source(name: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Заносит в REGISTRY новый источник задач.
    """
    def _decorator(factory: SourceFactory) -> SourceFactory:
        REGISTRY[name] = factory
        logger.info(f"Source registered: '{name}'")
        return factory
    return _decorator
