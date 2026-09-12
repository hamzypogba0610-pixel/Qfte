# app/calibration/methods/beta.py
"""
Beta Calibration pour QFTE.

Forme : logit(p_calibrated) = a*log(p) + b*log(1-p) + c
Plus flexible que Platt Scaling.
"""

from __future__ import annotations

import numpy as np
from scipy.special import expit
from scipy.optimize import minimize
from typing import Optional, Tuple


class BetaCalibrator:
    """
    Beta Calibration.
    """

    def __init__(self):
        self.params: Optional[Tuple[float, float, float]] = None
        self.fitted = False

    def fit(
        self,
        p_raw: np.ndarray,
        y: np.ndarray,
        sample_weight: Optional[np.ndarray] = None,
    ) -> "BetaCalibrator":
        """
        Entraîne le calibrateur.

        Args:
            p_raw: Probabilités brutes.
            y: Labels réels (0 ou 1).
            sample_weight: Poids optionnels.
        """
        eps = 1e-6
        p_clipped = np.clip(p_raw, eps, 1 - eps)

        def objective(params):
            a, b, c = params
            logit_p = a * np.log(p_clipped) + b * np.log(1 - p_clipped) + c
            p_calibrated = expit(logit_p)

            if sample_weight is not None:
                loss = -np.mean(
                    sample_weight
                    * (
                        y * np.log(p_calibrated + eps)
                        + (1 - y) * np.log(1 - p_calibrated + eps)
                    )
                )
            else:
                loss = -np.mean(
                    y * np.log(p_calibrated + eps)
                    + (1 - y) * np.log(1 - p_calibrated + eps)
                )
            return loss

        result = minimize(objective, [1.0, 1.0, 0.0], method="BFGS")
        self.params = tuple(result.x)  # type: ignore
        self.fitted = True
        return self

    def predict(self, p_raw: np.ndarray) -> np.ndarray:
        """
        Calibre de nouvelles probabilités.

        Args:
            p_raw: Probabilités brutes.

        Returns:
            Probabilités calibrées.
        """
        if not self.fitted:
            raise ValueError("BetaCalibrator must be fitted before use.")

        eps = 1e-6
        p_clipped = np.clip(p_raw, eps, 1 - eps)
        a, b, c = self.params  # type: ignore
        logit_p = a * np.log(p_clipped) + b * np.log(1 - p_clipped) + c
        return expit(logit_p)
