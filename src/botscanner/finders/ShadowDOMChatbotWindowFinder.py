from .BaseChatbotWindowFinder import BaseChatbotWindowFinder
from ..models.ChatbotWindowCandidate import ChatbotWindowCandidate
from .shadowDOM import _find_windows_candidates_as_shadowdom


class ShadowDOMChatbotWindowFinder(BaseChatbotWindowFinder):
    name = "shadow_dom"

    def find(self, driver, quiet: bool) -> list:
        print("searching shadow dom chatbot windows...")
        elements = _find_windows_candidates_as_shadowdom(driver, quiet)
        if not elements:
            return []

        return [
                ChatbotWindowCandidate(
                    source="dom",
                    context="shadow_dom",
                    element=el,
                    metadata={"html": el.get_attribute("outerHTML")}
                )
                for el in elements
            ]


