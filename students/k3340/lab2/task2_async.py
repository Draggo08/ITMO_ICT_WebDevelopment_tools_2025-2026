import asyncio
import ssl
import time

import aiohttp
import certifi
from bs4 import BeautifulSoup

from config import PARSE_URLS, WORKERS
from db import SessionLocal
from parse_utils import extract_title, save_parsed_page


async def parse_and_save(url: str, session: aiohttp.ClientSession) -> str:
    headers = {"User-Agent": "ITMO-Lab2-Parser/1.0"}
    async with session.get(url, timeout=aiohttp.ClientTimeout(total=30), headers=headers) as response:
        response.raise_for_status()
        html = await response.text()

    title = extract_title(html)

    db = SessionLocal()
    try:
        save_parsed_page(db, url, title)
    finally:
        db.close()

    print(f"{url} -> {title}")
    return title


async def run_all(urls: list[str]) -> None:
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    connector = aiohttp.TCPConnector(limit=WORKERS, ssl=ssl_context)
    async with aiohttp.ClientSession(connector=connector) as session:
        results = await asyncio.gather(*(parse_and_save(url, session) for url in urls), return_exceptions=True)
    for url, result in zip(urls, results, strict=True):
        if isinstance(result, Exception):
            print(f"{url} -> ERROR: {result}")


def main() -> None:
    started = time.perf_counter()
    asyncio.run(run_all(PARSE_URLS))
    elapsed = time.perf_counter() - started
    print(f"async parser: urls={len(PARSE_URLS)}, elapsed={elapsed:.4f}s, workers={WORKERS}")


if __name__ == "__main__":
    main()
