from bs4 import BeautifulSoup
from typing import Optional
import re


def extract_first_chatbot_text(html: str) -> Optional[str]:
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript", "meta", "link"]):
        tag.decompose()

    candidates = []

    for el in soup.find_all(["div", "span", "p", "button", "label"]):
        text = el.get_text(strip=True)
        if not text:
            continue

        candidates.append(text)

    for el in soup.find_all(True):
        for attr in ("aria-label", "title", "placeholder"):
            val = el.get(attr)
            if val:
                candidates.append(val.strip())

    for meta in soup.find_all("meta"):
        if meta.get("name") in {"description", "og:description"}:
            if meta.get("content"):
                candidates.append(meta["content"].strip())

    cleaned = []
    for text in candidates:
        t = re.sub(r"\s+", " ", text).strip()

        if len(t) < 3:
            continue

        if t.lower() in {
            "send",
            "typing",
            "close",
            "open",
            "chat",
            "message",
            "submit",
        }:
            continue

        if re.fullmatch(r"[0-9\W_]+", t):
            continue

        cleaned.append(t)

    return cleaned[0] if cleaned else None



def extract_first_chatbot_text_old(html: str) -> Optional[str]:
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
