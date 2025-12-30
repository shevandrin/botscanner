from bs4 import BeautifulSoup
from typing import Optional
import re


def extract_first_chatbot_text(html: str) -> Optional[str]:
    soup = BeautifulSoup(html, "html.parser")

    # 1. Locate chatbot body by semantic class match
    body = soup.find(
        "div",
        class_=re.compile(r"body", re.I)
    )

    if not body:
        return None

    # 2. Remove elements we explicitly want to ignore
    for tag in body.find_all([
        "button", "input", "textarea", "svg", "img"
    ]):
        tag.decompose()

    for header in body.find_all(["h1", "h2", "h3"]):
        header.decompose()

    # 3. Collect candidate text blocks
    for el in body.find_all(["div", "p", "span"], recursive=True):
        # Skip hidden or non-visible content
        if el.get("aria-hidden") == "true":
            continue

        text = el.get_text(strip=True)
        if not text:
            continue

        # Filter UI noise
        if text.lower() in {
            "typing",
            "powered by",
            "send",
            "type a message"
        }:
            continue

        return text

    return None
