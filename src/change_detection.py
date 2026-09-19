"""Stage 1: lightweight change detection by frame differencing.

Works on small grayscale frames (e.g. 96x96). Keeps only the previous frame in
memory, so it is cheap enough to run every cycle on a microcontroller-class
device (a C/Arduino port is still TO DO; this is the reference logic).
"""
import numpy as np


class ChangeDetector:
    def __init__(self, pixel_threshold: int = 25, min_changed_fraction: float = 0.01):
        # A pixel counts as "changed" if it moves by more than pixel_threshold.
        # The frame counts as an event if enough pixels changed.
        self.pixel_threshold = pixel_threshold
        self.min_changed_fraction = min_changed_fraction
        self._prev = None

    def update(self, frame):
        """Return (triggered: bool, changed_fraction: float)."""
        frame = np.asarray(frame, dtype=np.int16)
        if self._prev is None:
            self._prev = frame
            return False, 0.0
        diff = np.abs(frame - self._prev)
        fraction = float((diff > self.pixel_threshold).mean())
        self._prev = frame
        return fraction >= self.min_changed_fraction, fraction
