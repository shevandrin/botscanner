from .BaseChatbotAnchorFinder import BaseChatbotAnchorFinder
from ...models.BaseCandidate import ChatbotAnchorCandidateJS
from .find_shadow_anchor_candidates import _find_shadow_anchor_candidates


class ShadowChatbotAnchorFinder(BaseChatbotAnchorFinder):
    name = "shadow_chatbot_anchor"

    def find(self, driver, logger):
        logger.info("searching shadow dom chatbot anchors...")
        elements = _find_shadow_anchor_candidates(driver, logger)
        result = [
            ChatbotAnchorCandidateJS(
            index=-1,
            source="dom",
            context="main",
            element=None,
            tag=el.get('tag'),
            html=el.get('html'),
            strategy=self.__class__.__name__,
            clickable=el.get('clickable'),
            metadata={
                "identifiers": el.get('identifiers', {}),
                "keywordHits": el.get('keywordHits'),
                "text": el.get('text', '')[:200],
                "cursor": el.get('cursor'),
                "bounding": {
                "x": el.get('bounding', {}).get('x'),
                "y": el.get('bounding', {}).get('y'),
                "width": el.get('bounding', {}).get('width'),
                "height": el.get('bounding', {}).get('height')
                },
                "hostChain": el.get('hostChain', [])
            }
            ) for el in elements            
        ]

        # print shadow elements found
        for el in result:
            print(el.to_dict())
            #pass
        return result