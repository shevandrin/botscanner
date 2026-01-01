from dataclasses import dataclass, field
from typing import List, Optional, Any


@dataclass
class InteractionCandidate:
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
class ResolvedInteraction:
    selected: Optional[Any]
    candidates: List[InteractionCandidate] = field(default_factory=list)

    def to_dict(self):
        return {
            "selected": self.selected.value if self.selected else None,
            "candidates": [c.to_dict() for c in self.candidates]
        }


@dataclass
class ChatbotInteractions:
    user_input_message: Optional[ResolvedInteraction]
    chatbot_response: Optional[ResolvedInteraction]

    def to_dict(self):
        return {
            "user_input_message": self.user_input_message.to_dict() if self.user_input_message else None,
            "chatbot_response": self.chatbot_response.to_dict() if self.chatbot_response else None
        }
