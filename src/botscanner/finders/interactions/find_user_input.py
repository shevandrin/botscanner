from bs4 import BeautifulSoup
from typing import Optional, Dict


def find_user_input_field(html: str) -> Optional[Dict]:
    """
    Detects a user input field intended for typing chatbot messages.

    Detection priority:
    1. <textarea>
    2. <div> or <input> elements with 'textarea' in class name

    Args:
        html (str): HTML snapshot of the chatbot window

    Returns:
        dict with detection details or None if not found
    """

    soup = BeautifulSoup(html, "html.parser")

    textarea = soup.find("textarea")
    if textarea:
        return {
            "type": "textarea",
            "tag": "textarea",
            "class": textarea.get("class", []),
            "placeholder": textarea.get("placeholder"),
            "html": str(textarea)
        }

    fallback = soup.find(
        lambda tag: (
            (tag.name in ["div", "input"]
            and tag.get("class")
            and any("textarea" in cls.lower() for cls in tag.get("class")))
            or (tag.name == "input" and tag.get("type") == "text")
        )
    )

    if fallback:
        return {
            "type": "pseudo-textarea",
            "tag": fallback.name,
            "class": fallback.get("class", []),
            "placeholder": fallback.get("placeholder"),
            "html": str(fallback)
        }

    return None
