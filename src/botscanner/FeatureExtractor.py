from botscanner.models.ChatbotFeatures import ChatbotFeatures, PositionFeature, ResolvedFeature, FeatureCandidate
from botscanner.evaluators.get_location_chatbot_anchor import get_location_chatbot_anchor
from botscanner.finders.features.find_title_candidates import find_title_candidates
from botscanner.evaluators.eval_title_window import _evaluate_title_window
from botscanner.evaluators.eval_interface_type import _evaluate_interface_type
from botscanner.evaluators.get_location_chatbot_window import _get_chatbot_window_position
from botscanner.evaluators.get_first_chatbot_text import extract_first_chatbot_text

class FeatureExtractor:
    def __init__(self, driver, ChatbotDetector, logger):
        self.driver = driver
        self.anchor = ChatbotDetector.selected_anchor
        self.window = ChatbotDetector.selected_window
        self.logger = logger


    def extract_anchor_position(self) -> PositionFeature:
        loc = self.anchor.location
        if loc is not None:
            self.logger.info(f"Anchor position determined: {loc}")
            return PositionFeature(
                sector=loc)
        else:
            return PositionFeature(
                sector=None
        )

    def define_window_position(self) -> PositionFeature:
        if self.window is not None:
            sector = _get_chatbot_window_position(self.window.bounding_box)
            self.logger.info(f"Window position determined: {sector}")
            return PositionFeature(
                sector=sector)
        else:
            return PositionFeature(
                sector=None
        )

    def extract_window_type(self) -> str:
        if self.window is not None:
            return _evaluate_interface_type(self.window.dom_snapshot)
        else:
            return PositionFeature(
                sector=None
        )

        #if self.window.context == "iframe":
        #    return "iframe"
        #if self.window.context == "shadow":
        #    return "shadow_dom"
        #return "dom"

    def extract_title(self) -> ResolvedFeature:
        if self.window is None:
            return ResolvedFeature(
                selected=None,
                candidates=[])
        candidates = find_title_candidates(self.window.dom_snapshot)
        evaluated_candidates = [_evaluate_title_window(candidate) for candidate in candidates]
        self.logger.info(f"Found {(evaluated_candidates)} title candidates.")
        max_candidate = max(evaluated_candidates, key=lambda candidate: candidate.score, default=None)
        if max_candidate:
            self.logger.info(f"Selected title candidate: {max_candidate}")
            return ResolvedFeature(
                selected=max_candidate,
                candidates=evaluated_candidates)
        return ResolvedFeature(
            selected=None,
            candidates=evaluated_candidates)
    
    def extract_first_visible_text(self) -> str:
        if self.window is None:
            return None
        return extract_first_chatbot_text(self.window.dom_snapshot)
    
    def extract_avatar(self) -> ResolvedFeature:
        candidates = []
        return ResolvedFeature(
            selected=None,
            candidates=[])

    def extract(self) -> ChatbotFeatures:
        return ChatbotFeatures(
            anchor_position=self.extract_anchor_position(),
            window_position=self.define_window_position(),
            window_type=self.extract_window_type(),
            first_visible_text=self.extract_first_visible_text(),
            title=self.extract_title(),
            avatar=self.extract_avatar() # later
        )
