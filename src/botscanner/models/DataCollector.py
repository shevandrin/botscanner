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
    strategy: str
    score: float
    tag: str
    text: str
    title: Optional[str]
    aria_label: Optional[str]
    location: dict


# This classs is for properties of selected chatbot window
@dataclass
class ChatbotWindowProperties:
    window_type: str          # iframe | shadow | dom
    detected_via: str         # strategy / mechanism
    title: Optional[str]
    iframe_src: Optional[str]
    bounding_box: Optional[dict]


@dataclass
class StatsSnapshot:
    anchor_strategies: Dict[str, StrategyStats]
    #window_strategies: Dict[str, StrategyStats]
    #selected_anchor: Dict[str, Any] | None
    #selected_window: Dict[str, Any] | None

    def to_dict(self) -> dict:
        return asdict(self)
