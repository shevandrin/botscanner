from time import time
from botscanner.models.DataCollector import AnchorProperties, ChatbotWindowProperties, StatsSnapshot, StrategyStats
from botscanner.outcomes.writer import OutcomeWriter
from botscanner.selectors.select_anchor_chatbot_widget import select_anchor_candidate


class CandidateManager:

    def __init__(self, driver, writer: OutcomeWriter, logger):
        self.driver = driver
        self.writer = writer # outcome manager
        self.logger = logger
        self._candidates = []
        self._index = 0
        self.logger.info("CandidateManager initialized.")

    def add_candidates(self, candidates: list):
        self.logger.info("Adding candidates...")
        for c in candidates:
            c.index = self._index
            self._index += 1
            self._candidates.append(c)
        self.logger.info(f"Total candidates after addition: {len(self._candidates)}")   
        

    def process(self):
        self.logger.info(f"Processing {len(self._candidates)} candidates...")
        if not self._candidates:
            self.logger.info("No candidates to process.")
            return
        for candidate in self._candidates:
            self._process_candidate(candidate)
        candidates_data = [c.to_dict() for c in self._candidates]
        file_name = self._candidates[0].result_json_name
        self.logger.info(f"Saving candidates data to {file_name}")
        self.writer.save_json(file_name, candidates_data)

    def _process_candidate(self, candidate):
        self.logger.info("Processing next candidate:")
        candidate.evaluate()
        candidate.make_dom_snapshot(self.driver)
        candidate.save_dom(self.logger, self.driver, self.writer)
        candidate.save_screenshot_element(self.logger, self.driver, self.writer)
    def select_candidate(self, min_score: int = 0):
        valid = [c for c in self._candidates if c.score >= min_score]
        if not valid:
            return None

        def priority_key(c):
            iframe_priority = 1 if c.context == "iframe" else 0
            return (c.score, iframe_priority)

        return max(valid, key=priority_key)
    
    def _aggregate_by_strategy(self, candidates):
        stats = {}

        for c in candidates:
            stats.setdefault(c.strategy, []).append(c)

        result = {}

        for strategy, group in stats.items():
            scores = [c.score for c in group if c.score is not None]

            result[strategy] = StrategyStats(
                strategy_name=strategy,
                total_candidates=len(group),
                clickable_candidates=sum(1 for c in group if c.clickable == True),
                avg_score=sum(scores) / len(scores) if scores else None,
                score_distribution=self._score_distribution(scores)
            )

        return result

    def _score_distribution(self, scores) -> dict:
        distribution = {}
        for score in scores:
            rounded_score = round(score)
            distribution[rounded_score] = distribution.get(rounded_score, 0) + 1
        return distribution
    
    def build_stats_snapshot(self, domain: str) -> StatsSnapshot:
        return StatsSnapshot(
            domain=domain,
            strategies=self._aggregate_by_strategy(self._candidates)
        )

class CandidateManagerAnchor(CandidateManager):
    def select_candidate(self, min_score: int = 0):
        return select_anchor_candidate(self._candidates, min_score)
    