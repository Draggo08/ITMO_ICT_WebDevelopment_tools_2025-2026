import httpx

from app.celery_app import celery_app
from app.core.config import settings


@celery_app.task(name="parse_url")
def parse_url_task(url: str) -> dict:
    response = httpx.post(
        f"{settings.parser_url}/parse",
        params={"url": url},
        timeout=60.0,
    )
    response.raise_for_status()
    return response.json()
