from botscanner.models.ChatbotFeatures import ChatbotFeatures, PositionFeature, ResolvedFeature, FeatureCandidate
from botscanner.evaluators.get_location_chatbot_anchor import get_location_chatbot_anchor
from botscanner.finders.features.find_title_candidates import find_title_candidates
from botscanner.evaluators.eval_title_window import _evaluate_title_window
from botscanner.evaluators.eval_interface_type import _evaluate_interface_type
from botscanner.evaluators.get_location_chatbot_window import _get_chatbot_window_position
from botscanner.evaluators.get_first_chatbot_text import extract_first_chatbot_text
from botscanner.finders.interactions.find_user_input import find_user_input_field
from botscanner.models.ChatbotInteractions import ChatbotInteractions, InteractionCandidate, ResolvedInteraction

class InteractionsExtractor:
    def __init__(self, driver, ChatbotDetector, logger):
        self.driver = driver
        self.window = ChatbotDetector.selected_window
        self.logger = logger


    def find_input_message_candidates(self):
        result = find_user_input_field(self.window.dom_snapshot)

        candidates = []

        if result:
            candidates.append(
                InteractionCandidate(
                    source="dom",
                    value=result,
                    score=1.0,
                    metadata={
                        "detector": "find_user_input_field",
                        "type": result.get("type")
                    }
                )
            )

        if not candidates:
            return None

        selected = max(candidates, key=lambda c: c.score)

        return ResolvedInteraction(
            selected=selected,
            candidates=candidates
        )

    def find_chatbot_responses(self):
        return None

    def extract(self) -> ChatbotInteractions:
        return ChatbotInteractions(
            user_input_message=self.find_input_message_candidates(),
            chatbot_response=self.find_chatbot_responses()
        )
