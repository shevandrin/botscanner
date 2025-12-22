from abc import ABC, abstractmethod
from botscanner.models.BaseCandidate import ChatbotAnchorCandidate


class BaseChatbotAnchorFinder(ABC):
    name: str

    @abstractmethod
    def find(self, driver, logger) -> list[ChatbotAnchorCandidate]:
        pass