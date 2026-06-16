# Lab 3 — Docker, парсер и очереди

Упаковка FastAPI (lab1), PostgreSQL и парсера (lab2) в Docker. Вызов парсера синхронно через HTTP и асинхронно через Celery + Redis.

## Сервисы

| Сервис | Порт | Назначение |
|--------|------|------------|
| `api` | 8000 | FastAPI из lab1 + прокси к парсеру |
| `parser` | 8001 | Отдельный FastAPI-сервис парсера |
| `postgres` | 15432 | БД lab1 |
| `redis` | 6379 | Брокер и backend для Celery |
| `celery_worker` | — | Фоновая обработка задач парсинга |

## Запуск

Из каталога `students/k3340/lab3`:

```bash
docker compose up -d --build
docker compose ps
```

Остановить:

```bash
docker compose down
```

## API

Документация: http://127.0.0.1:8000/docs

### Синхронный парсинг (подзадача 2)

```bash
curl -X POST "http://127.0.0.1:8000/api/parse" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

### Асинхронный парсинг через Celery (подзадача 3)

```bash
# Поставить задачу в очередь
curl -X POST "http://127.0.0.1:8000/api/parse/async" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.python.org"}'

# Проверить статус (подставьте task_id из ответа)
curl "http://127.0.0.1:8000/api/parse/async/<task_id>"
```

### Парсер напрямую

```bash
curl -X POST "http://127.0.0.1:8001/parse?url=https://example.com"
```

### Проверка данных в БД

```bash
docker compose exec postgres psql -U postgres -d lab1_db \
  -c "SELECT id, url, title FROM parsed_pages ORDER BY id DESC LIMIT 5;"
```

## Структура

| Путь | Назначение |
|------|------------|
| `docker-compose.yml` | Оркестрация всех сервисов |
| `api/Dockerfile` | Образ FastAPI + Celery worker |
| `api/entrypoint.sh` | Миграции Alembic и запуск uvicorn/celery |
| `parser/Dockerfile` | Образ сервиса парсера |
| `parser/main.py` | HTTP-обёртка над `parse_and_save()` из lab2 |

## Связь с lab1 и lab2

- **lab1** — основное приложение, эндпоинты `/api/parse` и `/api/parse/async`
- **lab2** — логика `parse_and_save()` переиспользуется в контейнере `parser`
- **Celery** — задача `parse_url` вызывает parser по HTTP в фоне
