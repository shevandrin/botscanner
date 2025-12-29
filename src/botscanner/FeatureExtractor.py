from botscanner.models.ChatbotFeatures import ChatbotFeatures, PositionFeature, ResolvedFeature, FeatureCandidate
from botscanner.evaluators.get_location_chatbot_anchor import get_location_chatbot_anchor

class FeatureExtractor:
    def __init__(self, driver, ChatbotDetector, logger):
        self.driver = driver
        self.anchor = ChatbotDetector.selected_anchor
        self.window = ChatbotDetector.selected_window
        self.logger = logger


    def extract_anchor_position(self) -> PositionFeature:
        loc = get_location_chatbot_anchor(self.driver,self.anchor.element)
        if loc is not None:
            self.logger.info(f"Anchor position determined: {loc}")
            return PositionFeature(
                sector=loc)
        else:
            return PositionFeature(
                sector=None
        )

    def extract_window_type(self) -> str:
        if self.window.context == "iframe":
            return "iframe"
        if self.window.context == "shadow":
            return "shadow_dom"
        return "dom"

    def extract_title(self) -> ResolvedFeature:
        candidates = []
        # TODO: implement title extraction logic
        return ResolvedFeature(
            selected=None,
            candidates=[])
    
    def extract_avatar(self) -> ResolvedFeature:
        candidates = []
        return ResolvedFeature(
            selected=None,
            candidates=[])

    def extract(self) -> ChatbotFeatures:
        return ChatbotFeatures(
            anchor_position=self.extract_anchor_position(),
            window_position=None,  # later
            window_type=self.extract_window_type(),
            first_visible_text=None,  # later
            title=self.extract_title(),
            avatar=self.extract_avatar() # later
        )
