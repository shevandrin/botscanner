from .BaseChatbotWindowFinder import BaseChatbotWindowFinder
from ..models.ChatbotWindowCandidate import ChatbotWindowCandidate
from .iframe import _find_iframe_chatbot_windows


class IframeChatbotWindowFinder(BaseChatbotWindowFinder):
    name = "iframe_chatbot"

    def find(self, driver, quiet):
        print("searching iframe chatbot windows...")
        elements = _find_iframe_chatbot_windows(driver, quiet)
        return [
            ChatbotWindowCandidate(
                source="iframe",
                context="iframe",
                element=el,
                metadata={"html": el.get_attribute("outerHTML")}
            ) for el in elements            
        ]