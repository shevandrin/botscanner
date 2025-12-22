from time import time
from botscanner.outcomes.writer import OutcomeWriter


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

    def process(self):
        self.logger.info("Processing candidates...")
        self.logger.info(f"Number of candidates: {len(self._candidates)}")
        for candidate in self._candidates:
            self.logger.info("Processing a candidate:")
            self._process_candidate(candidate)
        candidates_data = [c.to_dict() for c in self._candidates]
        self.logger.info(f"Candidates data: {candidates_data}")
        file_name = self._candidates[0].result_json_name
        self.logger.info(file_name)
        self.writer.save_json(file_name, candidates_data)

    def _process_candidate(self, candidate):
        self.logger.info("Processing a candidate:")
        #candidate.capture(self.driver)
        candidate.evaluate()

        file_name = f"{candidate.dom_name}_{candidate.index}"
        self.logger.info(file_name)
        self.writer.save_dom(file_name, candidate.html)

        try:
            file_name = f"screenshot_{candidate.dom_name}_{candidate.index}"
            self.writer.save_element_screenshot(file_name, candidate.element)
        except Exception as e:
            self.logger.error(f"Failed to save element screenshot: {e}")

    def select_candidate(self, min_score: int = 1):
        valid = [c for c in self._candidates if c.score >= min_score]
        if not valid:
            return None
        return max(valid, key=lambda c: c.score)
    
class CandidateManagerAnchor(CandidateManager):
        
        def select_candidate(self, min_score: int = 1):
            valid_s1 = [c for c in self._candidates if c.score >= min_score and c.strategy == "SimpleDOMChatbotAnchorFinder"]
            if valid_s1:
                valid_s1.sort(key=lambda x: x.score, reverse=True)
                return valid_s1[0]
        
            valid_s2 = [c for c in self._candidates if c.score >= min_score and c.strategy == "ComputedStyleChatbotAnchorFinder"]
            if valid_s2:
                valid_s2.sort(key=lambda x: x.score, reverse=True)
                return valid_s2[0]
            return None