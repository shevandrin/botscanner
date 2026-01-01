from .BaseChatbotAnchorFinder import BaseChatbotAnchorFinder
from ...models.BaseCandidate import ChatbotAnchorCandidate
from .find_shadow_anchor_candidates import _find_shadow_anchor_candidates


class ShadowChatbotAnchor(BaseChatbotAnchorFinder):
    name = "shadow_chatbot_anchor"

    def find(self, driver, logger):
        logger.info("searching shadow dom chatbot anchors...")
        elements = _find_shadow_anchor_candidates(driver, logger)
        result = [
            ChatbotAnchorCandidate(
            index=-1,
            source="dom",
            context="main",
            element=None,
            tag=el.get('tag'),
            html=el.get('html'),
            strategy=self.__class__.__name__,
            clickable=el.get('clickable'),
            metadata={
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
        for el in elements:
            #print(el.get('tag'), el.get('keywordHits'), el.get('clickable'))
            pass
        return result