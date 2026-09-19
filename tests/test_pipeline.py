import numpy as np

from src.alert_logic import decide
from src.change_detection import ChangeDetector
from src.pipeline import Pipeline


class CountingClassifier:
    def __init__(self):
        self.calls = 0

    def predict(self, frame, hint=None):
        self.calls += 1
        return "animal", 0.9


def flat(v=100, size=96):
    return np.full((size, size), v, dtype=np.uint8)


def test_static_scene_never_triggers():
    d = ChangeDetector()
    for _ in range(10):
        triggered, _ = d.update(flat())
        assert not triggered


def test_large_change_triggers():
    d = ChangeDetector()
    d.update(flat())
    frame = flat()
    frame[20:60, 20:60] = 220
    triggered, fraction = d.update(frame)
    assert triggered and fraction > 0.1


def test_tiny_change_is_ignored():
    d = ChangeDetector()
    d.update(flat())
    frame = flat()
    frame[0:4, 0:4] = 250  # well under 1% of pixels
    assert not d.update(frame)[0]


def test_classifier_not_called_when_idle():
    clf = CountingClassifier()
    p = Pipeline(clf)
    for i in range(20):
        p.process(flat(), f"t{i}")
    assert clf.calls == 0 and p.stats["idle"] == 20


def test_classifier_called_on_change_and_alert_logged():
    clf = CountingClassifier()
    p = Pipeline(clf)
    p.process(flat(), "t0")
    changed = flat()
    changed[10:70, 10:70] = 230
    event = p.process(changed, "t1")
    assert clf.calls == 1 and event["action"] == "alert"


def test_decide_thresholds():
    assert decide("human", 0.9) == "alert"
    assert decide("human", 0.5) == "discard"
    assert decide("nothing", 0.99) == "discard"
