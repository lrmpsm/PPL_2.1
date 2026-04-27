from .exceptions import InvalidTaskPriorityError

class TimeAsText:
    """
    Non-data descriptor для ленивого форматирования datetime аттрибутов
    в человекочитаемый вид.

    Обеспечивает кеширование вычисленного отформаттированного значения
    до момента изменения любого аттрибута публичного API модели Task.
    """
    def __init__(self, source_attr: str, fmt: str = "%d.%m.%Y %H:%M:%S %Z") -> None:
        self.source_attr = source_attr
        self.fmt = fmt

    def __set_name__(self, owner: type, name:str) -> None:
        self.name = name

    def __get__(self, instance: object | None, owner: type) -> object:
        if instance is None:
            return self

        value = getattr(instance, self.source_attr).strftime(self.fmt)

        instance.__dict__[self.name] = value

        return value


class ValidatedField:
    """
    Базовый класс для data descriptors.

    Setter реализован таким способом, что:
    - сначала валидируется присваеваемое значение
    - потом оно присваивается аттрибуту данного валидатора
    - если у класса, в котором используется валидатор,
    есть метод _touch, то он вызывается.
    """
    def __set_name__(self, owner: type, name: str) -> None:
        self.private_name = f"_{name}"

    def __get__(self, instance: object | None, owner: type) -> object:
        if instance is None:
            return self

        return getattr(instance, self.private_name)

    def __set__(self, instance: object, value: object) -> None:
        self.validate(value)
        setattr(instance, self.private_name, value)

        touch = getattr(instance, "_touch", None)
        if callable(touch):
            touch()

    def validate(self, value: object) -> None:
        raise NotImplementedError


class NonEmptyLimitedString(ValidatedField):
    """
    Data descriptor для непустых текстовых полей с
    ограниченной длинной символов.

    :max_length - максимальное кол-во символов аттрибута
    :error_cls - класс исключения, который вызывается
    при ошибках валидации
    :field_name - имя аттрибута, которое будет фигурировать в
    текстах ошибки
    """
    def __init__(
            self,
            max_length: int = 1000,
            error_cls: type[Exception] = ValueError,
            field_name: str = "Value",
        ) -> None:
        self.max_length = max_length
        self.error_cls = error_cls
        self.field_name = field_name

    def validate(self, value: object) -> None:
        if type(value) is not str:
            raise self.error_cls(f"{self.field_name} must be a string.")
        if value.strip() == "":
            raise self.error_cls(f"{self.field_name} must contain at least 1 non-space symbol.")
        if len(value.strip()) > self.max_length:
            raise self.error_cls(f"{self.field_name} mustn't contain more than {self.max_length} symbols.")



class Priority(ValidatedField):
    """
    Data descriptor для приоритета.

    Возможно задание максимального и
    минимального значений, доступных
    для соответствующего атрибута.
    """
    def __init__(
            self,
            min_value: int = 1,
            max_value: int = 5,
        ) -> None:
        self.min_value = min_value
        self.max_value = max_value


    def validate(self, value: object) -> None:
        if type(value) is not int:
            raise InvalidTaskPriorityError("Priority must be an integer.")

        if not (self.min_value <= value <= self.max_value):
            raise InvalidTaskPriorityError(
                f"Priority must be in [{self.min_value}; {self.max_value}]."
            )
