from .BaseChatbotWindowFinder import BaseChatbotWindowFinder
from ..models.ChatbotWindowCandidate import ChatbotWindowCandidate
from .framework_patterns import _find_windows_candidates_by_framework


class SimpleDOMChatbotWindowFinder(BaseChatbotWindowFinder):
    name = "simple_dom"

    def find(self, driver, quiet):
        print("searching simple dom chatbot windows...")
        elements = _find_windows_candidates_by_framework(driver, quiet)
        return [
            ChatbotWindowCandidate(
                source="dom",
                context="main",
                element=el,
                metadata={"html": el.get_attribute("outerHTML")}
            ) for el in elements            
        ]
