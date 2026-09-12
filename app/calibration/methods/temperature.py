# app/calibration/methods/temperature.py
"""
Temperature Scaling pour QFTE.

Particulièrement utile pour les modèles multiclasses.
p_calibrated = sigmoid(logits / T)
"""

from __future__ import annotations

import numpy as np
from scipy.special import expit
from scipy.optimize import minimize
from typing import Optional


class TemperatureScaler:
    """
    Temperature Scaling.
    """

    def __init__(self):
        self.temperature: float = 1.0
        self.fitted = False

    def fit(self, logits: np.ndarray, y: np.ndarray) -> "TemperatureScaler":
        """
        Entraîne le calibrateur.

        Args:
            logits: Logits bruts du modèle (avant sigmoid).
            y: Labels réels (0 ou 1).
        """

        def objective(T):
            if T <= 0:
                return 1e10
            p = expit(logits / T)
            eps = 1e-15
            loss = -np.mean(
                y * np.log(p + eps) + (1 - y) * np.log(1 - p + eps)
            )
            return loss

        result = minimize(
            objective,
            1.0,
            method="L-BFGS-B",
            bounds=[(0.1, 10.0)],
        )
        self.temperature = float(result.x)
        self.fitted = True
        return self

    def predict(self, logits: np.ndarray) -> np.ndarray:
        """
        Calibre de nouvelles probabilités à partir des logits.

        Args:
            logits: Logits bruts.

        Returns:
            Probabilités calibrées.
        """
        if not self.fitted:
            raise ValueError("TemperatureScaler must be fitted before use.")

        return expit(logits / self.temperature)
