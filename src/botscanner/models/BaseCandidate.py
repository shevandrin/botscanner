from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Literal
from botscanner.evaluators.eval_iframe_chatbot_window import _evaluate_iframe_candidate
from selenium.webdriver.remote.webelement import WebElement


@dataclass
class BaseCandidate:
    index: int
    source: str
    context: str
    element: Any
    tag: str
    html: str

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
class AnchorCandidate(BaseCandidate):
    result_json_name: str = "anchor_candidates"
    dom_name: str = "anchor_candidate"
    def evaluate(self):
        # TODO: Implement evaluation logic for AnchorCandidate
        return self