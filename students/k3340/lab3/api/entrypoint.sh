#!/bin/sh
set -e

echo "Running database migrations..."
PYTHONPATH=. alembic upgrade head

if [ "$1" = "celery" ]; then
    echo "Starting Celery worker..."
    exec celery -A app.celery_app.celery_app worker --loglevel=info
fi

echo "Starting FastAPI..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
