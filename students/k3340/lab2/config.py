import os
from pathlib import Path

from dotenv import load_dotenv

LAB2_DIR = Path(__file__).resolve().parent
LAB1_DIR = LAB2_DIR.parent / "lab1"

load_dotenv(LAB1_DIR / ".env")
load_dotenv(LAB2_DIR / ".env")

DATABASE_URL = os.environ["DATABASE_URL"]

TOTAL_N = 10_000_000_000_000
WORKERS = os.cpu_count() or 4

PARSE_URLS = [
    "https://example.com",
    "https://www.python.org",
    "https://docs.python.org/3/",
    "https://www.w3.org",
    "https://en.wikipedia.org/wiki/Python_(programming_language)",
    "https://quotes.toscrape.com",
    "https://www.rust-lang.org",
    "https://fastapi.tiangolo.com",
]
