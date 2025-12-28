from abc import ABC, abstractmethod
from botscanner.models.BaseCandidate import ChatbotWindowCandidate


class BaseChatbotWindowFinder(ABC):
    name: str

    @abstractmethod
    def find(self, driver, logger) -> list[ChatbotWindowCandidate]:
        pass