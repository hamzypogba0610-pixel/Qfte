# app/calibration/hybrid/adaptive_calibration.py
"""
Calibration adaptative en ligne pour QFTE.

S'adapte automatiquement aux changements de distribution
via une fenêtre glissante et une recalibration périodique.
"""

from __future__ import annotations

import numpy as np
from typing import Optional, Any, Deque
from collections import deque


class AdaptiveCalibrator:
    """
    Calibration adaptative en ligne.
    """

    def __init__(
        self,
        window_size: int = 500,
        update_frequency: int = 50,
    ):
        self.window_size = window_size
        self.update_frequency = update_frequency
        self.history: Deque[tuple] = deque(maxlen=window_size)
        self.calibrator: Optional[Any] = None
        self.fitted = False
        self.n_updates = 0

    def update(self, p_raw: float, y: int) -> None:
        """
        Met à jour le calibrateur avec une nouvelle observation.

        Args:
            p_raw: Probabilité brute.
            y: Label réel (0 ou 1).
        """
        self.history.append((p_raw, y))
        self.n_updates += 1

        # Recalibrer périodiquement
        if (
            len(self.history) >= self.window_size
            and self.n_updates % self.update_frequency == 0
        ):
            self._recalibrate()

    def _recalibrate(self) -> None:
        """Recalibre sur la fenêtre glissante."""
        from ..methods.platt import PlattScaler

        data = list(self.history)
        p_raw = np.array([d for d in data])
        y = np.array([d[1] for d in data])

        # Pondération temporelle (plus récent = plus important)
        weights = np.linspace(0.5, 1.5, len(data))

        self.calibrator = PlattScaler()
        self.calibrator.fit(p_raw, y, sample_weight=weights)
        self.fitted = True

    def predict(self, p_raw: float) -> float:
        """
        Calibre une probabilité.

        Args:
            p_raw: Probabilité brute.

        Returns:
            Probabilité calibrée.
        """
        if not self.fitted:
            return p_raw  # Pas de calibration si pas assez de données

        return float(self.calibrator.predict(np.array([p_raw])))
