# TODO: Take heuristics values from patterns
def _evaluate_iframe_candidate(candidate: dict) -> dict:
    html = candidate["html"].lower()
    score = 0
    evidence = []

    if "chat" in html:
        score += 3
        evidence.append("keyword 'chat'")

    if "bot" in html:
        score += 3
        evidence.append("keyword 'bot'")
    
    if "window" in html:
        score += 2
        evidence.append("keyword 'window'")
    
    if "messeng" in html:
        score += 1
        evidence.append("keyword 'messeng'")

    if "ask" in html:
        score += 1
        evidence.append("keyword 'ask'")
    
    return {
        **candidate,
        "score": score,
        "evidence": evidence
    }
