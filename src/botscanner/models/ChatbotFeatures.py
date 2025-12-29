from dataclasses import dataclass, field
from typing import List, Optional, Any


@dataclass
class FeatureCandidate:
    source: str
    value: Any
    score: float
    metadata: dict = field(default_factory=dict)

    def to_dict(self):
        return {
            "source": self.source,
            "value": self.value,
            "score": self.score,
            "metadata": self.metadata
        }


@dataclass
class ResolvedFeature:
    selected: Optional[Any]
    candidates: List[FeatureCandidate] = field(default_factory=list)

    def to_dict(self):
        return {
            "selected": self.selected.value if self.selected else None,
            "candidates": [c.to_dict() for c in self.candidates]
        }


@dataclass
class PositionFeature:
    sector: Optional[str]     # "bottom-right", "top-left", etc.

    def to_dict(self):
        return self.__dict__


@dataclass
class ChatbotFeatures:
    anchor_position: Optional[PositionFeature]
    window_position: Optional[PositionFeature]
    window_type: Optional[str]
    first_visible_text: Optional[str]

    title: ResolvedFeature
    avatar: ResolvedFeature

    def to_dict(self):
        return {
            "anchor_position": self.anchor_position.to_dict() if self.anchor_position else None,
            "window_position": self.window_position.to_dict() if self.window_position else None,
            "window_type": self.window_type,
            "first_visible_text": self.first_visible_text,
            "title": self.title.to_dict(),
            "avatar": self.avatar.to_dict()
        }
