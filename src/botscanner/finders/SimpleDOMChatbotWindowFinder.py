from .BaseChatbotWindowFinder import BaseChatbotWindowFinder
from ..models.BaseCandidate import ChatbotWindowCandidate
from .framework_patterns import _find_windows_candidates_by_framework


class SimpleDOMChatbotWindowFinder(BaseChatbotWindowFinder):
    name = "simple_dom"

    def find(self, driver, quiet):
        print("searching simple dom chatbot windows...")
        elements = _find_windows_candidates_by_framework(driver, quiet)
        result = [
            ChatbotWindowCandidate(
                index=-1,
                source="dom",
                context="main",
                element=el,
                tag=el.tag_name,
                html=el.get_attribute("outerHTML")
            ) for el in elements            
        ]
        return result