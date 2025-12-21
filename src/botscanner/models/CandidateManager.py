from time import time
from botscanner.outcomes.writer import OutcomeWriter
from botscanner.utils import vprint


class CandidateManager:

    def __init__(self, driver, writer: OutcomeWriter, quiet=True):
        self.driver = driver
        self.writer = writer # outcome manager
        self.quiet = quiet
        self._candidates = []
        self._index = 0
        print("CandidateManager initialized.")

    def add_candidates(self, candidates: list):
        print("Adding candidates...")
        for c in candidates:
            c.index = self._index
            self._index += 1
            self._candidates.append(c)

    def process(self):
        print("Processing candidates1...")
        print(len(self._candidates))
        for candidate in self._candidates:
            print("call process a candidate:")
            self._process_candidate(candidate)
        candidates_data = [c.to_dict() for c in self._candidates]
        print("candidates_data:")
        print(candidates_data)
        file_name = self._candidates[0].result_json_name
        print(file_name)
        self.writer.save_json(file_name, candidates_data)

    def _process_candidate(self, candidate):
        print("process a candidate:")
        #candidate.capture(self.driver)
        candidate.evaluate()

        file_name = f"{candidate.dom_name}_{candidate.index}"
        print(file_name)
        self.writer.save_dom(file_name, candidate.html)

        try:
            file_name = f"screenshot_{candidate.dom_name}_{candidate.index}"
            self.writer.save_element_screenshot(file_name, candidate.element)
        except Exception as e:
            vprint(f"Failed to save element screenshot: {e}", self.quiet)

    def select_candidate(self, min_score: int = 1):
        valid = [c for c in self._candidates if c.score >= min_score]
        if not valid:
            return None
        return max(valid, key=lambda c: c.score)
