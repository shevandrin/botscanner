from dataclasses import asdict, dataclass, field
from typing import Dict, Any, Optional
from botscanner.utils import get_element_attribute


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
    index: Optional[int]
    strategy: Optional[str]
    score: Optional[float]
    tag: Optional[str]
    text: Optional[str]
    title: Optional[str]
    id: Optional[str]
    class_attr: Optional[str]
    name: Optional[str]
    aria_label: Optional[str]
    location: Optional[dict]

    def __init__(self, driver, element, logger):
        self.index = element.index if element else None
        self.strategy = element.strategy if element else None
        self.score = element.score if element else None
        self.tag = element.tag if element else None
        self.text = get_element_attribute(element.element, "innerText")
        self.title = get_element_attribute(element.element, "title")
        self.id = get_element_attribute(element.element, "id")
        self.class_attr = get_element_attribute(element.element, "class")
        self.name = get_element_attribute(element.element, "name")
        self.aria_label = get_element_attribute(element.element, "aria-label")
        self.location = None  # Initialize location attribute
        logger.info("Capturing properties of selected anchor element...")
        
        
    def to_dict(self) -> dict:
        return asdict(self)


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
    selected_anchor: Optional[AnchorProperties] = None

    def to_dict(self) -> dict:
        return {
            "anchor": self.anchor.to_dict()["strategies"],
            "window": self.window.to_dict()["strategies"],
            "selected_anchor": self.selected_anchor.to_dict() if self.selected_anchor else None
        }