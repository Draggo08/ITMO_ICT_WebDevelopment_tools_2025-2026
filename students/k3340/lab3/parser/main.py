import os
import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query

ROOT = Path(__file__).resolve().parents[2]
LAB1_DIR = ROOT / "lab1"
LAB2_DIR = ROOT / "lab2"

for path in (LAB1_DIR, LAB2_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@postgres:5432/lab1_db",
)

from parse_utils import parse_and_save  # noqa: E402

app = FastAPI(title="Lab3 Parser Service", version="1.0.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/parse")
def parse(url: str = Query(..., min_length=1)) -> dict[str, str]:
    try:
        title = parse_and_save(url)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error

    return {
        "message": "Parsing completed",
        "url": url,
        "title": title,
    }
