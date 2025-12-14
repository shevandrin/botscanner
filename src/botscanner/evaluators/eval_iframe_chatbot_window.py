def _evaluate_iframe_candidate(candidate: dict) -> dict:
    html = candidate["html"].lower()
    score = 0
    evidence = []

    if "chat" in html:
        score += 3
        evidence.append("keyword 'chat'")
    
    if "window" in html:
        score += 2
        evidence.append("keyword 'window'")
    
    return {
        **candidate,
        "score": score,
        "evidence": evidence
    }
