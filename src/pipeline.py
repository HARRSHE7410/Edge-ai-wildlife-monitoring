"""Ties the three stages together: change detection -> classifier -> alert logic."""
from .alert_logic import EventLogger, decide
from .change_detection import ChangeDetector


class Pipeline:
    def __init__(self, classifier, detector=None, threshold: float = 0.7):
        self.classifier = classifier
        self.detector = detector or ChangeDetector()
        self.threshold = threshold
        self.logger = EventLogger()
        self.stats = {"frames": 0, "idle": 0, "classifier_calls": 0, "alerts": 0, "discarded": 0}

    def process(self, frame, timestamp: str, hint=None):
        self.stats["frames"] += 1
        triggered, fraction = self.detector.update(frame)
        if not triggered:
            self.stats["idle"] += 1
            return None
        self.stats["classifier_calls"] += 1
        label, confidence = self.classifier.predict(frame, hint=hint)
        action = decide(label, confidence, self.threshold)
        self.stats["alerts" if action == "alert" else "discarded"] += 1
        return self.logger.log(timestamp, label, confidence, action, fraction)
