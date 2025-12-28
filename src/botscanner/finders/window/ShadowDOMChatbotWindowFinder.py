from .BaseChatbotWindowFinder import BaseChatbotWindowFinder
from ...models.BaseCandidate import ChatbotWindowCandidate
from .find_window_by_shadowDOM import _find_windows_candidates_as_shadowdom


class ShadowDOMChatbotWindowFinder(BaseChatbotWindowFinder):
    name = "shadow_dom"

    def find(self, driver, logger) -> list:
        logger.info("searching shadow dom chatbot windows...")
        elements = _find_windows_candidates_as_shadowdom(driver, logger)
        if not elements:
            return []

        return [
                ChatbotWindowCandidate(
                    index=-1,
                    source="dom",
                    context="shadow_dom",
                    element=el,
                    tag=el.tag_name,
                    html=el.get_attribute("outerHTML"),
                    strategy=self.__class__.__name__,
                )
                for el in elements
            ]



