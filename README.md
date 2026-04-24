# Лабораторная работа №1
* Тема: Источники задач и контракты
* Дисциплина: "Программирование на языке Python"
* Семестр: 2

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

### Вывести список доступных команд
```bash
    python -m src.main
```

## Реализация

### Задача

Задача представлена моделью `Task` (`src/models/task.py`).

Имеет поля
- `id`: str
- `payload`: Any

### Источники

Реализованы следующие источники задач:
- `generator` - генерация `n` задач со случайным `payload` (`src/sources/generator.py`)
- `stdin` - чтение задач из стандартного ввода (`src/sources/stdin.py`)
- `file-jsonl` - чтение задач из `jsonl`-файла (`src/sources/json.py`)

Контракт `TaskSource` для источников описан с помощью `typing.Protocol` (`src/contracts/task_source.py`).

Предусмотрено добавление новых источников в `REGISTRY` (`src/sources/repository.py`).

Во время получения задач каждый источник проверяется на соответствие контракту (`src/inbox/core.py`)

### Тесты

Написаны unit-тесты для:
- Интерфейса командной строки (`tests/test_cli.py`)
- Приема задач из нескольких источников (`tests/test_inbox.py`)
- Источников задач:
    * Генератора (`tests/test_generator.py`)
    * Стандартного ввода (`tests/test_stdin.py`)
    * `jsonl`-файлов (`tests/test_json.py`)

### Логирование

В проекте используется стандартный модуль `logging`.

Конфигурация находится в файле `src/logging_config.py`

Логи записываются в файл `logs/shell.log`
