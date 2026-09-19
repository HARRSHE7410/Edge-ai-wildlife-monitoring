"""Stage 3: decision logic and auditable event log."""
import json
from typing import List, Optional

ALERT_CLASSES = {"animal", "human", "vehicle"}


def decide(label: str, confidence: float, threshold: float = 0.7) -> str:
    """Return 'alert' or 'discard'. Every decision is logged, not just alerts."""
    if label not in ALERT_CLASSES:
        return "discard"
    if confidence < threshold:
        return "discard"
    return "alert"


class EventLogger:
    """Logs every trigger with class, confidence, and action (transparency).
    No images are stored by default (privacy)."""

    def __init__(self):
        self.events: List[dict] = []

    def log(self, timestamp: str, label: str, confidence: float, action: str,
            changed_fraction: Optional[float] = None) -> dict:
        event = {
            "timestamp": timestamp,
            "class": label,
            "confidence": confidence,
            "action": action,
            "changed_fraction": None if changed_fraction is None else round(changed_fraction, 4),
        }
        self.events.append(event)
        return event

    def to_json(self) -> str:
        return json.dumps(self.events, indent=2)
