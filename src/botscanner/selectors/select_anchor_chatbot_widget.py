from botscanner.evaluators.eval_anchor_chatbot_widget import _evaluate_anchor_candidate


def select_anchor_chatbot_widget(candidates: dict, quiet: bool = True) -> dict:
    """
    This functions selects the chatbot widget launcher element from the candidates found by different strategies.

    Strategie 1 has priority over Strategie 2.
    """
    for strategy in ["strategy_1", "strategy_2"]:
        if strategy in candidates and candidates[strategy]:
            for candidate in candidates[strategy]:
                candidates[strategy][candidates[strategy].index(candidate)] = _evaluate_anchor_candidate(candidate)
            candidates[strategy].sort(key=lambda x: x['score'], reverse=True)
    return candidates