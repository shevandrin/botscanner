from .BaseChatbotAnchorFinder import BaseChatbotAnchorFinder
from ..models.BaseCandidate import ChatbotAnchorCandidate
from .find_anchor_candidates_by_computed_style import _find_anchor_candidates_by_computed_style


class ComputedStyleChatbotAnchorFinder(BaseChatbotAnchorFinder):
    name = "computed_style_anchor_seeker"

    def find(self, driver, quiet):
        print("searching dom chatbot anchors by computed style ...")
        elements = _find_anchor_candidates_by_computed_style(driver, quiet)
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