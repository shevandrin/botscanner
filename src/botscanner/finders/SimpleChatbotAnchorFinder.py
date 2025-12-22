from .BaseChatbotAnchorFinder import BaseChatbotAnchorFinder
from ..models.BaseCandidate import ChatbotAnchorCandidate
from .find_anchor_candidates_by_hooks import _find_anchor_candidates_by_hooks


class SimpleDOMChatbotAnchorFinder(BaseChatbotAnchorFinder):
    name = "simple_anchor_seeker"

    def find(self, driver, logger):
        logger.info("searching simple dom chatbot anchors...")
        elements = _find_anchor_candidates_by_hooks(driver, logger)
        result = [
            ChatbotAnchorCandidate(
                index=-1,
                source="dom",
                context="main",
                element=el,
                tag=el.tag_name,
                html=el.get_attribute("outerHTML"),
                strategy=self.__class__.__name__,
            ) for el in elements            
        ]
        return result