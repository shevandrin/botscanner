from bs4 import BeautifulSoup

def has_visible_text(html: str) -> bool:
    if not html:
        return False

    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(strip=True)

    return len(text) > 0


# TODO: Take heuristics values from patterns
def _evaluate_anchor_candidate(candidate: dict) -> dict:
    html = candidate["html"].lower()
    score = 0
    evidence = []

    if "chat" in html:
        score += 3
        evidence.append("keyword 'chat'")

    if "button" in html:
        score += 1
        evidence.append("keyword 'button'")

    if "widget" in html:
        score += 1
        evidence.append("keyword 'widget'")

    if "widget-launcher" in html:
        score += 4
        evidence.append("keyword 'widget-launcher'")

    if has_visible_text(html):
        score += 0.5
        evidence.append("contains visible text")

    if "intercom-launcher-frame " in html:
        score += 5
        evidence.append("keyword 'intercom-launcher-frame'")

    if not candidate['clickable']:
        score = 0
        evidence = ["not clickable"]
    
    return {
        **candidate,
        "score": score,
        "evidence": evidence
    }