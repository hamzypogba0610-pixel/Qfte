# app/calibration/recalibration/recalibration_strategy.py
"""
Stratégies de recalibration pour QFTE.

Définit quand et comment recalibrer le modèle.
"""

from __future__ import annotations

import numpy as np
from typing import Any, Optional, Protocol
from .drift_detection import DriftDetector


class RecalibrationStrategy(Protocol):
    """
    Interface pour une stratégie de recalibration.
    """

    def should_recalibrate(self, drift_detected: bool) -> bool:
        """
        Décide s'il faut recalibrer.

        Args:
            drift_detected: Dérive détectée ou non.

        Returns:
            True si recalibration nécessaire.
        """
        ...


class PeriodicStrategy:
    """
    Recalibration périodique (tous les N échantillons).
    """

    def __init__(self, period: int = 500):
        self.period = period
        self.counter = 0

    def should_recalibrate(self, drift_detected: bool = False) -> bool:
        self.counter += 1
        if self.counter >= self.period:
            self.counter = 0
            return True
        return False


class DriftBasedStrategy:
    """
    Recalibration déclenchée par détection de dérive.
    """

    def __init__(self, drift_detector: DriftDetector):
        self.drift_detector = drift_detector
        self.cooldown = 0
        self.min_samples_between_recalib: int = 200

    def should_recalibrate(
        self,
        drift_detected: Optional[bool] = None,
        probs: Optional[np.ndarray] = None,
        labels: Optional[np.ndarray] = None,
    ) -> bool:
        if self.cooldown > 0:
            self.cooldown -= 1
            return False

        if drift_detected is None and probs is not None and labels is not None:
            drift_detected, _ = self.drift_detector.detect(probs, labels)

        if drift_detected:
            self.cooldown = self.min_samples_between_recalib
            return True

        return False


class HybridStrategy:
    """
    Combinaison de recalibration périodique et basée sur la dérive.
    """

    def __init__(
        self,
        periodic_strategy: PeriodicStrategy,
        drift_strategy: DriftBasedStrategy,
    ):
        self.periodic_strategy = periodic_strategy
        self.drift_strategy = drift_strategy

    def should_recalibrate(
        self,
        drift_detected: Optional[bool] = None,
        probs: Optional[np.ndarray] = None,
        labels: Optional[np.ndarray] = None,
    ) -> bool:
        periodic = self.periodic_strategy.should_recalibrate()
        drift = self.drift_strategy.should_recalibrate(
            drift_detected=drift_detected,
            probs=probs,
            labels=labels,
        )
        return periodic or drift
