# Лабораторные работы
* Дисциплина: "Программирование на языке Python"
* Семестр: 2

В данном `README` содержится описание:
- реализованного функционала в рамках лабораторных работ;
- структуры проекта;
- способов запуска проекта и тестов.

## Структура проекта

```
.
├── README.md
├── pyproject.toml
├── sources
│   └── tasks.jsonl
├── src
│   ├── __init__.py
│   ├── cli.py
│   ├── contracts
│   │   ├── __init__.py
│   │   └── task_source.py
│   ├── inbox
│   │   ├── __init__.py
│   │   └── core.py
│   ├── logging_config.py
│   ├── main.py
│   ├── models
│   │   ├── __init__.py
│   │   └── task.py
│   └── sources
│       ├── __init__.py
│       ├── generator.py
│       ├── json.py
│       ├── repository.py
│       └── stdin.py
├── tests
│   ├── __init__.py
│   ├── test_generator.py
│   ├── test_inbox.py
│   ├── test_cli.py
│   ├── test_json.py
│   └── test_stdin.py
└── uv.lock
```

## Запуск проекта

### Проверка прохождения тестов

Запуск тестов:
```bash
python -m pytest
```

Проверка покрытия:
```bash
python -m pytest --cov=src --cov-report=term-missing
```

### Вывести список доступных команд CLI
```bash
python -m src.main
```

## Лабораторная работа №1
* Тема: Источники задач и контракты

### Реализация

#### Задача

Задача представлена моделью `Task` (`src/models/task.py`).

Имеет поля:
- `id: str` - идентификатор задачи
- `payload: Any` - данные задачи

#### Источники задач

Реализованы следующие источники задач:
- `generator` - генерация `n` задач со случайным `payload` (`src/sources/generator.py`)
- `stdin` - чтение задач из стандартного ввода (`src/sources/stdin.py`)
- `file-jsonl` - чтение задач из `jsonl`-файла (`src/sources/json.py`)

#### Контракт источников

Контракт `TaskSource` для источников описан с помощью `typing.Protocol` (`src/contracts/task_source.py`).

В контракт входят:
- `name: str` - имя источника
- `fetch()` - метод получения задач

Для возможности runtime-проверки используется `@runtime_checkable`.

Во время получения задач каждый источник проверяется на соответствие контракту (`src/inbox/core.py`).

#### Реестр источников

Для регистрации источников используется `REGISTRY` (`src/sources/repository.py`).

Добавление новых источников выполняется через декоратор `register_source`.

Это позволяет добавлять новые источники без изменения кода `InboxApp`.

#### CLI

В проекте реализован CLI (`src/cli.py`).

Поддерживаются команды:
- `plugins` - вывод списка доступных источников
- `read` - чтение задач из выбранных источников

Для команды `read` можно выбрать источники:
- `--stdin`
- `--jsonl`
- `--generator`

### Тесты

Написаны unit-тесты для:
- интерфейса командной строки (`tests/test_cli.py`)
- приема задач из нескольких источников (`tests/test_inbox.py`)
- источников задач:
    - генератора (`tests/test_generator.py`)
    - стандартного ввода (`tests/test_stdin.py`)
    - `jsonl`-файлов (`tests/test_json.py`)

Тесты проверяют:
- создание задач из разных источников;
- соответствие источников контракту `TaskSource`;
- runtime-проверку контракта;
- регистрацию источников;
- работу CLI-команд.

### Логирование

В проекте используется стандартный модуль `logging`.

Конфигурация находится в файле `src/logging_config.py`.

Логи записываются в файл `logs/shell.log`.
