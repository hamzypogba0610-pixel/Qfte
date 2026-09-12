# app/calibration/manager.py
"""
Manager principal de calibration pour QFTE.

Orchestre :
- Le choix de la méthode de calibration.
- L'entraînement et la prédiction.
- La recalibration adaptative.
"""

from __future__ import annotations

import numpy as np
from typing import Optional, Literal, Dict, Any
from pathlib import Path

from .methods.platt import PlattScaler
from .methods.isotonic import IsotonicScaler
from .methods.beta import BetaCalibrator
from .methods.temperature_scaling import TemperatureScaling
from .methods.histogram import HistogramCalibrator

from .hybrid.ensemble_calibration import EnsembleCalibrator
from .hybrid.adaptive_calibration import AdaptiveCalibrator

from .recalibration.drift_detection import DriftDetector
from .recalibration.recalibration_strategy import (
    PeriodicStrategy,
    DriftBasedStrategy,
    HybridStrategy,
)
from .recalibration.recalibration_manager import RecalibrationManager


class CalibrationManager:
    """
    Gestionnaire principal de calibration.
    """

    def __init__(
        self,
        method: Literal["platt", "isotonic", "beta", "temperature", "histogram", "ensemble", "adaptive"] = "platt",
        recalibrate: bool = True,
        recalibration_period: int = 500,
        drift_detection: bool = True,
        buffer_size: int = 2000,
    ):
        """
        Args:
            method: Méthode de calibration.
            recalibrate: Activer la recalibration.
            recalibration_period: Période de recalibration (si périodique).
            drift_detection: Activer la détection de dérive.
            buffer_size: Taille du buffer pour la recalibration.
        """
        self.method = method
        self.recalibrate = recalibrate
        self.buffer_size = buffer_size

        # Calibrateur principal
        self.calibrator = self._create_calibrator(method)

        # Recalibration
        self.recalibration_manager: Optional[RecalibrationManager] = None
        if recalibrate:
            self._setup_recalibration(
                recalibration_period=recalibration_period,
                drift_detection=drift_detection,
            )

        self.fitted = False

    def _create_calibrator(
        self,
        method: str,
    ) -> Any:
        """Crée le calibrateur selon la méthode."""
        if method == "platt":
            return PlattScaler()
        elif method == "isotonic":
            return IsotonicScaler()
        elif method == "beta":
            return BetaCalibrator()
        elif method == "temperature":
            return TemperatureScaling()
        elif method == "histogram":
            return HistogramCalibrator()
        elif method == "ensemble":
            return EnsembleCalibrator()
        elif method == "adaptive":
            return AdaptiveCalibrator()
        else:
            raise ValueError(f"Unknown calibration method: {method}")

    def _setup_recalibration(
        self,
        recalibration_period: int,
        drift_detection: bool,
    ) -> None:
        """Configure la recalibration."""
        drift_detector = DriftDetector(method="ks") if drift_detection else None

        periodic_strategy = PeriodicStrategy(period=recalibration_period)
        drift_strategy = DriftBasedStrategy(
            drift_detector=drift_detector
        ) if drift_detector else None

        if drift_strategy:
            strategy = HybridStrategy(periodic_strategy, drift_strategy)
        else:
            strategy = periodic_strategy

        self.recalibration_manager = RecalibrationManager(
            strategy=strategy,
            drift_detector=drift_detector,
            buffer_size=self.buffer_size,
        )

    def fit(
        self,
        p_raw: np.ndarray,
        y: np.ndarray,
        sample_weight: Optional[np.ndarray] = None,
    ) -> "CalibrationManager":
        """
        Entraîne le calibrateur.

        Args:
            p_raw: Probabilités brutes.
            y: Labels réels (0 ou 1).
            sample_weight: Poids optionnels.
        """
        self.calibrator.fit(p_raw, y, sample_weight=sample_weight)
        self.fitted = True

        # Initialiser le buffer de recalibration
        if self.recalibration_manager:
            for p, label in zip(p_raw, y):
                self.recalibration_manager.update(float(p), int(label))

        return self

    def predict(self, p_raw: np.ndarray) -> np.ndarray:
        """
        Calibre des probabilités.

        Args:
            p_raw: Probabilités brutes.

        Returns:
            Probabilités calibrées.
        """
        if not self.fitted:
            raise ValueError("CalibrationManager must be fitted before use.")

        return self.calibrator.predict(p_raw)

    def update(
        self,
        p_raw: float,
        y: int,
    ) -> bool:
        """
        Met à jour le calibrateur en ligne.

        Args:
            p_raw: Probabilité brute.
            y: Label réel (0 ou 1).

        Returns:
            True si une recalibration a eu lieu.
        """
        if not self.recalibrate or not self.recalibration_manager:
            return False

        return self.recalibration_manager.update(p_raw, y)

    def save(self, filepath: str) -> None:
        """Sauvegarde le calibrateur."""
        import pickle

        with open(filepath, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load(filepath: str) -> "CalibrationManager":
        """Charge un calibrateur sauvegardé."""
        import pickle

        with open(filepath, "rb") as f:
            return pickle.load(f)
