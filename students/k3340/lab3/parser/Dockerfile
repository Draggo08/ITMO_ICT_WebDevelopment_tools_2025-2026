FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY lab3/parser/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY lab1/app /app/lab1/app
COPY lab2/parse_utils.py /app/lab2/parse_utils.py
COPY lab2/db.py /app/lab2/db.py
COPY lab2/config.py /app/lab2/config.py
COPY lab3/parser/main.py /app/lab3/parser/main.py

ENV PYTHONPATH=/app/lab1:/app/lab2
ENV DATABASE_URL=postgresql+psycopg2://postgres:postgres@postgres:5432/lab1_db

EXPOSE 8001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--app-dir", "/app/lab3/parser"]
