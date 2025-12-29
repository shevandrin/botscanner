from bs4 import BeautifulSoup
from botscanner.models.ChatbotFeatures import FeatureCandidate
from typing import List


ALLOWED_TITLE_TAGS = {"div", "h1", "h2", "h3", "h4", "h5", "h6"}


def find_title_candidates(html: str) -> List[FeatureCandidate]:
    soup = BeautifulSoup(html, "html.parser")

    candidates = []

    for el in soup.find_all(ALLOWED_TITLE_TAGS):
        text = el.get_text(strip=True)
        if not text:
            continue

        # Attribute-based heuristics
        for attr in ["id", "class", "name", "aria-label"]:
            val = el.get(attr)
            if val and "title" in str(val).lower():
                candidates.append(
                    FeatureCandidate(
                        source=attr,
                        value=text,
                        score=0.0,
                        metadata={
                            "tag": el.name,
                            "matched_on": "title",
                            "html": str(el),
                            "class": el.get("class"),
                            "id": el.get("id"),
                            "name": el.get("name"),
                            "aria-label": el.get("aria-label"),
                        }
                    )
                )

        # Role-based heuristics
        role = el.get("role")
        if role in ("head", "title") or el.name.startswith("h"):
            candidates.append(
                FeatureCandidate(
                    source="role",
                    value=text,
                    score=0.0,
                    metadata={
                        "tag": el.name,
                        "role": role
                    }
                )
            )

    return candidates
