from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Literal
from botscanner.evaluators.eval_iframe_chatbot_window import _evaluate_iframe_candidate
from botscanner.evaluators.eval_anchor_chatbot_widget import _evaluate_anchor_candidate
from selenium.webdriver.remote.webelement import WebElement
from botscanner.utils import _is_element_clickable


@dataclass
class BaseCandidate:
    index: int
    source: str
    context: str
    element: Any
    tag: str
    html: str
    clickable: Optional[bool] = None
    strategy: Optional[str] = None
    dom_name: str = "base_candidate"

    score: int = 0
    evidence: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def evaluate(self) -> None:
        """
        Evaluate the candidate and update its score and evidence.
        Override in subclasses.
        """
        raise NotImplementedError("Subclasses should implement this method.")
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "index": self.index,
            "source": self.source,
            "context": self.context,
            "tag": self.tag,
            "html": self.html,
            "score": self.score,
            "evidence": self.evidence,
            "clickable": self.clickable,
            "strategy": self.strategy,
            **self.metadata,
        }
    
    def save_screenshot_element(self, logger, driver, writer) -> None:
        """
        Save a screenshot of the candidate's web element.
        """
        if isinstance(self.element, WebElement):
            try:
                file_name = f"screenshot_{self.dom_name}_{self.index}"
                writer.save_element_screenshot(file_name, self.element, logger, driver)
            except Exception as e:
                logger.error(f"Failed to save element screenshot: {e}")

    def save_dom(self, logger, writer) -> None:
        """
        Save the DOM content of the candidate.
        """
        try:
            file_name = f"dom_{self.dom_name}_{self.index}"
            writer.save_dom(file_name, self.html)
            self.logger.info(f"Dom content saved to {file_name}")
        except Exception as e:
            logger.error(f"Failed to save DOM content: {e}")

@dataclass
class ChatbotWindowCandidate(BaseCandidate):
    result_json_name: str = "chatbot_window_candidates"
    dom_name: str = "chatbot_window_candidate"
    def evaluate(self):
        result = _evaluate_iframe_candidate(self.to_dict())
        self.score = result["score"]
        self.evidence = result["evidence"]
        return self


@dataclass
class ChatbotAnchorCandidate(BaseCandidate):
    clickable: Optional[bool] = None
    result_json_name: str = "anchor_candidates"
    dom_name: str = "anchor_candidate"
    
    def __post_init__(self):
        if self.clickable is None and isinstance(self.element, WebElement):
            try:
                self.clickable = _is_element_clickable(self.element)
            except Exception:
                self.clickable = False

    def evaluate(self):
        result = _evaluate_anchor_candidate(self.to_dict())
        self.score = result["score"]
        self.evidence = result["evidence"]
        return self