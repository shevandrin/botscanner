from dataclasses import asdict, dataclass, field
from typing import Dict, Any, Optional


@dataclass
class RunMetadata:
    url: str
    timestamp: str
    browser: str
    user_agent: Optional[str]


@dataclass
class StrategyStats:
    strategy_name: str
    total_candidates: int = 0
    clickable_candidates: int = 0
    avg_score: Optional[float] = None
    score_distribution: dict = field(default_factory=dict)    
   

# This calss is for properties of selected anchor
@dataclass
class AnchorProperties:
    strategy: Optional[str]
    score: Optional[float]
    tag: Optional[str]
    text: Optional[str]
    title: Optional[str]
    aria_label: Optional[str]
    location: Optional[dict]


# This classs is for properties of selected chatbot window
@dataclass
class ChatbotWindowProperties:
    window_type: Optional[str]          
    detected_via: Optional[str]
    title: Optional[str]
    iframe_src: Optional[str]
    bounding_box: Optional[dict]


@dataclass
class StatsSnapshot:
    domain: str
    strategies: Dict[str, StrategyStats]

    def to_dict(self) -> dict:
        return {
            "domain": self.domain,
            "strategies": {k: asdict(v) for k, v in self.strategies.items()}
        }


@dataclass
class FinalReport:
    anchor: StatsSnapshot
    window: StatsSnapshot

    def to_dict(self) -> dict:
        return {
            "anchor": self.anchor.to_dict()["strategies"],
            "window": self.window.to_dict()["strategies"],
        }