def _evaluate_title_window(candidate: dict) -> dict:
    score = 0

    if "chat" in candidate.value.lower() or "assist" in candidate.value.lower():
        score += 2

    if "{" in candidate.value.lower() or "}" in candidate.value.lower():
        score -= 0.25

    candidate.score = score
    
    return candidate
    