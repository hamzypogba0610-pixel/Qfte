# app/calibration/recalibration/recalibration_manager.py
"""
Gestionnaire de recalibration pour QFTE.

Orchestre la détection de dérive, la stratégie de recalibration,
et l'entraînement du nouveau calibrateur.
"""

from __future__ import annotations

import numpy as np
from typing import Any, Optional, Dict
from collections import deque
from .drift_detection import DriftDetector
from .recalibration_strategy import (
    RecalibrationStrategy,
    PeriodicStrategy,
    DriftBasedStrategy,
    HybridStrategy,
)


class RecalibrationManager:
    """
    Gestionnaire de recalibration.
    """

    def __init__(
        self,
        strategy: RecalibrationStrategy,
        drift_detector: Optional[DriftDetector] = None,
        buffer_size: int = 2000,
    ):
        self.strategy = strategy
        self.drift_detector = drift_detector
        self.buffer_size = buffer_size

        # Buffer pour les données de recalibration
        self.prob_buffer: deque = deque(maxlen=buffer_size)
        self.label_buffer: deque = deque(maxlen=buffer_size)

        self.calibrator: Optional[Any] = None
        self.n_updates = 0

    def update(
        self,
        p_raw: float,
        y: int,
    ) -> bool:
        """
        Met à jour le gestionnaire avec une nouvelle observation.

        Args:
            p_raw: Probabilité brute.
            y: Label réel (0 ou 1).

        Returns:
            True si une recalibration a été déclenchée.
        """
        self.prob_buffer.append(p_raw)
        self.label_buffer.append(y)
        self.n_updates += 1

        drift_detected = False
        if (
            self.drift_detector is not None
            and len(self.prob_buffer) >= 500
        ):
            probs = np.array(list(self.prob_buffer)[-500:])
            labels = np.array(list(self.label_buffer)[-500:])

            # Définir une référence si pas encore fait
            if self.drift_detector.reference_probs is None:
                self.drift_detector.set_reference(
                    probs[:-100], labels[:-100]
                )

            drift_detected, _ = self.drift_detector.detect(
                probs[-100:], labels[-100:]
            )

        should_recalib = self.strategy.should_recalibrate(
            drift_detected=drift_detected,
            probs=np.array(list(self.prob_buffer)),
            labels=np.array(list(self.label_buffer)),
        )

        if should_recalib:
            self._recalibrate()
            return True

        return False

    def _recalibrate(self) -> None:
        """Recalibre le calibrateur."""
        from ..methods.platt import PlattScaler

        if len(self.prob_buffer) < 200:
            return

        probs = np.array(list(self.prob_buffer))
        labels = np.array(list(self.label_buffer))

        # Pondération temporelle
        weights = np.linspace(0.5, 1.5, len(probs))

        self.calibrator = PlattScaler()
        self.calibrator.fit(probs, labels, sample_weight=weights)

    def predict(self, p_raw: float) -> float:
        """
        Calibre une probabilité.

        Args:
            p_raw: Probabilité brute.

        Returns:
            Probabilité calibrée.
        """
        if self.calibrator is None:
            return p_raw

        return float(self.calibrator.predict(np.array([p_raw])))
