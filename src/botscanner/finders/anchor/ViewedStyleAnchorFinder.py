from .BaseChatbotAnchorFinder import BaseChatbotAnchorFinder
from ...models.BaseCandidate import ChatbotAnchorCandidate
from .find_anchor_candidates_as_viewed import _find_anchor_candidates_as_viewed


class ViewedStyleChatbotAnchorFinder(BaseChatbotAnchorFinder):
    name = "viewed_style_anchor_seeker"

    def find(self, driver, logger):
        logger.info("searching dom chatbot anchors by viewed style ...")
        elements = _find_anchor_candidates_as_viewed(driver, logger)
        result = [
            ChatbotAnchorCandidate(
            index=-1,
            source="dom",
            context="main",
            element=el,
            tag=el.tag_name,
            html="",
            #html=el.get_attribute("outerHTML"),
            strategy=self.__class__.__name__,
            ) for el in elements            
        ]
        return result