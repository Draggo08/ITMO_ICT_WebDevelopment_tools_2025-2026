# k3340 — общая инфраструктура

## PostgreSQL в Docker

Из этой папки:

```bash
docker compose up -d
docker compose ps
```

Остановить (данные в volume сохранятся):

```bash
docker compose down
```

Удалить и контейнер, и данные:

```bash
docker compose down -v
```

### Подключение

| Параметр | Значение |
|----------|----------|
| Host | `localhost` |
| Port | `15432` (в контейнере 5432; снаружи 15432, чтобы не конфликтовать с локальным Postgres) |
| User | `postgres` |
| Password | `postgres` |
| Database | `lab1_db` |

URL для `.env` в lab1 и lab2:

```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:15432/lab1_db
```

## Быстрый тест (lab1 + lab2)

```bash
# 1. БД
cd students/k3340
docker compose up -d

# 2. Миграции
cd lab1
source .venv/bin/activate
PYTHONPATH=. alembic upgrade head

# 3. Lab2 — задача 1 (без БД)
cd ../lab2
source .venv/bin/activate   # если ещё нет: python -m venv .venv && pip install -r requirements.txt
python task1_threading.py
python task1_multiprocessing.py
python task1_async.py

# 4. Lab2 — задача 2 (парсинг + БД)
python task2_threading.py
python task2_multiprocessing.py
python task2_async.py

# 5. Проверить данные в БД
cd ..
docker compose exec postgres psql -U postgres -d lab1_db -c "SELECT id, url, title FROM parsed_pages;"
```

## Lab1 API (опционально)

```bash
cd lab1
uvicorn app.main:app --reload
# http://127.0.0.1:8000/docs
```
