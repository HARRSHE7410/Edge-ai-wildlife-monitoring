"""Stage 2: classifier interface.

STATUS: the real TinyML classifier (quantized int8 MobileNet-style CNN, trained
and exported with Edge Impulse) is PLANNED and NOT built. This file defines the
interface it must satisfy and provides a SimulatedClassifier used ONLY by the
simulation so the rest of the pipeline can be exercised.
"""
import random
from typing import Optional, Tuple

CLASSES = ("animal", "human", "vehicle", "nothing")


class SimulatedClassifier:
    """DEMO ONLY. Reads the simulator's ground-truth hint and returns it with a
    made-up confidence, plus occasional low-confidence mistakes. It does not look
    at pixels and says nothing about real model accuracy."""

    def __init__(self, seed: int = 0, error_rate: float = 0.1):
        self._rng = random.Random(seed)
        self.error_rate = error_rate

    def predict(self, frame, hint: Optional[str] = None) -> Tuple[str, float]:
        if hint not in CLASSES:
            hint = "nothing"
        if self._rng.random() < self.error_rate:
            return self._rng.choice(CLASSES), round(self._rng.uniform(0.30, 0.65), 2)
        return hint, round(self._rng.uniform(0.72, 0.98), 2)
