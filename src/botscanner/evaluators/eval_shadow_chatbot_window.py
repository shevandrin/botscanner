from bs4 import BeautifulSoup
def _evaluate_shadow_candidate(candidate: dict) -> dict:
    html = candidate["html"].lower()
    score = 0
    evidence = []

    if "chat" in html:
        score += 3
        evidence.append("keyword 'chat'")
    
    if "window" in html:
        score += 2
        evidence.append("keyword 'window'")
    
    if "messeng" in html:
        score += 1
        evidence.append("keyword 'messeng'")

    if "ask" in html:
        score += 1
        evidence.append("keyword 'ask'")

    soup = BeautifulSoup(candidate["html"], 'html.parser')
    first_element = soup.find()
    if first_element and first_element.find():
        score += 1
        evidence.append("has child elements")
    
    return {
        **candidate,
        "score": score,
        "evidence": evidence
    }
