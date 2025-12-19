from abc import ABC, abstractmethod
from botscanner.models.ChatbotWindowCandidate import ChatbotWindowCandidate


class BaseChatbotWindowFinder(ABC):
    name: str

    @abstractmethod
    def find(self, driver, quiet: bool) -> list[ChatbotWindowCandidate]:
        pass