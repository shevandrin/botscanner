from .BaseChatbotWindowFinder import BaseChatbotWindowFinder
from ..models.BaseCandidate import ChatbotWindowCandidate
from .iframe import _find_iframe_chatbot_windows


class IframeChatbotWindowFinder(BaseChatbotWindowFinder):
    name = "iframe_chatbot"

    def find(self, driver, quiet):
        print("searching iframe chatbot windows...")
        elements = _find_iframe_chatbot_windows(driver, quiet)
        return [
            ChatbotWindowCandidate(
                index=-1,
                source="iframe",
                context="iframe",
                element=el,
                tag=el.tag_name,
                html=el.get_attribute("outerHTML"),
                strategy=self.__class__.__name__,
            ) for el in elements            
        ]