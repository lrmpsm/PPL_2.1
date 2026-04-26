import inspect
from collections.abc import Callable

def optional_param_names(func: Callable) -> list[str]:
    """
    Возвращает имена всех опциональных параметров функции.
    Пропускает self, cls, *args, **kwargs.
    """
    sig = inspect.signature(func)
    optional = []

    for name, param in sig.parameters.items():
        if name in ("self", "cls"):
            continue
        if param.kind in (
            inspect.Parameter.VAR_POSITIONAL,
            inspect.Parameter.VAR_KEYWORD,
        ):
            continue

        if param.default is not inspect.Parameter.empty:
            optional.append(name)

    return optional


def required_param_names(func: Callable) -> list[str]:
    """
    Возвращает имена всех обязательных параметров функции.
    Пропускает self, cls, *args, **kwargs.
    """
    sig = inspect.signature(func)
    required = []

    for name, param in sig.parameters.items():
        if name in ("self", "cls"):
            continue
        if param.kind in (
            inspect.Parameter.VAR_POSITIONAL,
            inspect.Parameter.VAR_KEYWORD,
        ):
            continue

        if param.default is inspect.Parameter.empty:
            required.append(name)

    return required


def param_names(func: Callable) -> list[str]:
    """
    Возвращает имена всех параметров функции.
    Пропускает self и cls.
    """

    sig = inspect.signature(func)
    names = []

    for name, param in sig.parameters.items():
        if name in ("self", "cls"):
            continue
        names.append(name)

    return names

def is_integer(x: str) -> bool:
    try:
        int(x)
        return True
    except (ValueError, TypeError):
        return False
