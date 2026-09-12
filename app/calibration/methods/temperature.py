# app/calibration/methods/temperature_scaling.py
"""
Temperature Scaling pour la calibration.

Ajuste une température T pour adoucir/renforcer les probabilités.
"""

from __future__ import annotations

import numpy as np
from typing import Optional
from scipy.optimize import minimize_scalar


class TemperatureScaling:
    """
    Temperature Scaling.

    Trouve une température T > 0 qui minimise le Log Loss.
    """

    def __init__(self):
        self.temperature: float = 1.0
        self.fitted = False

    def _apply_temperature(
        self,
        p_raw: np.ndarray,
        temperature: float,
    ) -> np.ndarray:
        """
        Applique la température aux probabilités.

        Args:
            p_raw: Probabilités brutes.
            temperature: Température T.

        Returns:
            Probabilités calibrées.
        """
        # Conversion en logits
        eps = 1e-15
        p_raw = np.clip(p_raw, eps, 1 - eps)
        logits = np.log(p_raw / (1 - p_raw))

        # Division par T
        scaled_logits = logits / temperature

        # Retour en probabilités
        return 1 / (1 + np.exp(-scaled_logits))

    def _log_loss(
        self,
        y: np.ndarray,
        p: np.ndarray,
    ) -> float:
        """Log Loss."""
        eps = 1e-15
        p = np.clip(p, eps, 1 - eps)
        return float(
            -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))
        )

    def fit(
        self,
        p_raw: np.ndarray,
        y: np.ndarray,
        sample_weight: Optional[np.ndarray] = None,
    ) -> "TemperatureScaling":
        """
        Trouve la température optimale.

        Args:
            p_raw: Probabilités brutes.
            y: Labels réels (0 ou 1).
            sample_weight: Poids optionnels (non utilisés ici).
        """
        p_raw = np.asarray(p_raw, dtype=float)
        y = np.asarray(y, dtype=float)

        def objective(T):
            p_calib = self._apply_temperature(p_raw, T)
            return self._log_loss(y, p_calib)

        # Recherche de T dans [0.1, 10]
        result = minimize_scalar(
            objective,
            bounds=(0.1, 10.0),
            method="bounded",
        )

        self.temperature = float(result.x)
        self.fitted = True
        return self

    def predict(self, p_raw: np.ndarray) -> np.ndarray:
        """
        Calibre avec la température apprise.

        Args:
            p_raw: Probabilités brutes.

        Returns:
            Probabilités calibrées.
        """
        if not self.fitted:
            raise ValueError("TemperatureScaling must be fitted before use.")

        return self._apply_temperature(p_raw, self.temperature)
