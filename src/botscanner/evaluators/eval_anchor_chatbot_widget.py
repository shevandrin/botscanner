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
    
    if not candidate['clickable']:
        score = 0
        evidence = ["not clickable"]
    
    return {
        **candidate,
        "score": score,
        "evidence": evidence
    }