from botscanner.evaluators.eval_anchor_chatbot_widget import _evaluate_anchor_candidate


def select_anchor_candidate(candidates, min_score: int = 1):
    """
    Select best candidate across all strategies.
    Priority rule:
      1) highest max score wins
      2) if tie → strategy priority:
         SimpleDOMChatbotAnchorFinder >
         ComputedStyleChatbotAnchorFinder >
         ViewedStyleChatbotAnchorFinder
         ShadowChatbotAnchorFinder
    """

    strategy_priority = [
        "SimpleDOMChatbotAnchorFinder",
        "ComputedStyleChatbotAnchorFinder",
        "ViewedStyleChatbotAnchorFinder",
        "ShadowChatbotAnchorFinder"
    ]

    # Group candidates by strategy
    by_strategy = {s: [] for s in strategy_priority}

    for c in candidates:
        if c.score >= min_score and c.strategy in by_strategy:
            by_strategy[c.strategy].append(c)

    # Compute best score per strategy
    best_per_strategy = []
    for strategy, candidates in by_strategy.items():
        if not candidates:
            continue

        best_score = max(c.score for c in candidates)
        best_candidates = [c for c in candidates if c.score == best_score]

        best_per_strategy.append((strategy, best_score, best_candidates))

    if not best_per_strategy:
        return None

    # Find global maximum score
    global_max = max(item[1] for item in best_per_strategy)

    # Filter strategies that achieved that score
    tied_strategies = [
        item for item in best_per_strategy if item[1] == global_max
    ]

    # Resolve tie using predefined priority
    for strategy in strategy_priority:
        for strat, score, candidates in tied_strategies:
            if strat == strategy:
                return candidates[0]  # already best score

    return None


def select_candidate_old(self, min_score: int = 1):
    valid_s1 = [c for c in self._candidates if c.score >= min_score and c.strategy == "SimpleDOMChatbotAnchorFinder"]
    if valid_s1:
        valid_s1.sort(key=lambda x: x.score, reverse=True)
        return valid_s1[0]

    valid_s2 = [c for c in self._candidates if c.score >= min_score and c.strategy == "ComputedStyleChatbotAnchorFinder"]
    if valid_s2:
        valid_s2.sort(key=lambda x: x.score, reverse=True)
        return valid_s2[0]

    valid_s3 = [c for c in self._candidates if c.score >= 0 and c.strategy == "ViewedStyleChatbotAnchorFinder"]
    self.logger.info(f"ViewedStyleChatbotAnchorFinder valid candidates count: {len(valid_s3)}")
    if valid_s3:
        valid_s3.sort(key=lambda x: x.score, reverse=True)
        return valid_s3[0]
    
    return None