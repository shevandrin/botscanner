from .BaseChatbotWindowFinder import BaseChatbotWindowFinder
from ...models.BaseCandidate import ChatbotWindowCandidate
from .find_window_by_framework_patterns import _find_window_candidates_by_framework


class FrameworkChatbotWindowFinder(BaseChatbotWindowFinder):
    name = "framework"

    def find(self, driver, logger):
        logger.info("searching framework chatbot windows...")
        elements = _find_window_candidates_by_framework(driver, logger)
        result = [
            ChatbotWindowCandidate(
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