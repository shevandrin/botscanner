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