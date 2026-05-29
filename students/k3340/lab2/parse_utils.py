import certifi
import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

from db import ParsedPage, SessionLocal


def extract_title(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    title_tag = soup.find("title")
    if title_tag is None or not title_tag.string:
        return "(no title)"
    return title_tag.get_text(strip=True)


def save_parsed_page(db: Session, url: str, title: str) -> None:
    row = db.query(ParsedPage).filter(ParsedPage.url == url).one_or_none()
    if row is None:
        db.add(ParsedPage(url=url, title=title))
    else:
        row.title = title
    db.commit()


def parse_and_save(url: str) -> str:
    """Load page, parse <title>, save to DB, print result."""
    response = requests.get(
        url,
        timeout=30,
        headers={"User-Agent": "ITMO-Lab2-Parser/1.0"},
        verify=certifi.where(),
    )
    response.raise_for_status()
    title = extract_title(response.text)

    db = SessionLocal()
    try:
        save_parsed_page(db, url, title)
    finally:
        db.close()

    print(f"{url} -> {title}")
    return title
