# Lab 2 — Потоки, процессы, асинхронность

Сравнение `threading`, `multiprocessing` и `asyncio` на CPU-задаче (сумма 1…10¹³) и I/O-задаче (парсинг страниц в PostgreSQL из lab1).

## Подготовка

0. PostgreSQL в Docker (из `students/k3340`):

```bash
cd ..
docker compose up -d
```

1. В **lab1** применить миграцию с таблицей `parsed_pages`:

```bash
cd ../lab1
PYTHONPATH=. alembic upgrade head
```

2. В **lab2** создать venv, установить зависимости:

```bash
cd ../lab2
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Скопировать `.env` из lab1 (или `.env.example`) — нужен тот же `DATABASE_URL`.

## Структура

| Файл | Назначение |
|------|------------|
| `task1_threading.py` | Сумма диапазона, `threading` |
| `task1_multiprocessing.py` | Сумма диапазона, `multiprocessing.Pool` |
| `task1_async.py` | Сумма диапазона, `asyncio` + `to_thread` |
| `task2_threading.py` | Парсинг URL, `ThreadPoolExecutor` |
| `task2_multiprocessing.py` | Парсинг URL, `multiprocessing.Pool` |
| `task2_async.py` | Парсинг URL, `aiohttp` + `asyncio.gather` |
| `sum_utils.py` | `calculate_sum()`, разбиение диапазона |
| `parse_utils.py` | `parse_and_save()` для sync-вариантов |
| `db.py` | Подключение к БД lab1, модель `ParsedPage` |

Таблица `parsed_pages` (lab1): `id`, `url` (unique), `title`, `parsed_at`.

## Запуск

Из каталога `lab2`:

```bash
python task1_threading.py
python task1_multiprocessing.py
python task1_async.py

python task2_threading.py
python task2_multiprocessing.py
python task2_async.py
```

## Задача 1 — особенности

- Диапазон `1..10_000_000_000_000` делится на `cpu_count()` частей.
- `calculate_sum(start, end)` использует формулу арифметической прогрессии за O(1) на чанк (цикл по каждому числу невозможен при таком N).
- Эталон: `N * (N + 1) // 2`.

### Таблица времени (задача 1)

Замеры на вашей машине (пример — подставьте свои значения):

| Подход | Время (с) | Комментарий |
|--------|-----------|-------------|
| threading | ~0.0006 | GIL: при микросекундной работе на чанк ускорения нет |
| multiprocessing | ~0.14 | Накладные расходы на старт процессов больше выигрыша |
| async (`to_thread`) | ~0.002 | Похоже на threading через пул потоков |

При формуле O(1) все три варианта завершаются почти мгновенно — на защите важно объяснить: **параллелизм выигрывает, когда чанк реально грузит CPU**; при чистой формуле накладные расходы на потоки/процессы доминируют.

## Задача 2 — особенности

- Список URL в `config.py` (`PARSE_URLS`).
- `parse_and_save(url)`: HTTP → `<title>` → INSERT/UPDATE в `parsed_pages` → print.
- Каждый поток/процесс открывает **свою** сессию SQLAlchemy.

### Таблица времени (задача 2)

| Подход | Время (с) | Комментарий |
|--------|-----------|-------------|
| threading | _заполнить_ | I/O: потоки перекрывают ожидание сети |
| multiprocessing | _заполнить_ | Часто медленнее из-за fork + отдельных процессов |
| async (aiohttp) | _заполнить_ | Обычно лучший для многих HTTP без блокировки event loop |

## Выводы для отчёта

1. **CPU-bound** (сумма): без тяжёлого цикла в чанке GIL не даёт threading выиграть; `multiprocessing` обходит GIL; `async` сам по себе CPU не ускоряет (нужен executor).
2. **I/O-bound** (HTTP + БД): `async` и `threading` эффективнее `multiprocessing`.
3. **GIL** — один интерпретатор Python на поток; процессы — отдельная память и свой GIL.

## Связь с lab1

Модель `ParsedPage` и миграция `20260528_02` в `students/k3340/lab1/`. Lab2 пишет в ту же БД через `DATABASE_URL`.
