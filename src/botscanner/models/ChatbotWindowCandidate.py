from dataclasses import dataclass, field
from typing import Optional, Literal
from selenium.webdriver.remote.webelement import WebElement

@dataclass
class ChatbotWindowCandidate:
    source: Literal["dom", "shadow", "iframe"]
    context: Literal["main", "shadow", "iframe"]

    element: Optional[WebElement] = None
    iframe_element: Optional[WebElement] = None

    score: float = 0.0
    metadata: dict = field(default_factory=dict)

    def short_label(self) -> str:
        return f"{self.source}:{self.context} score={self.score:.2f}"
