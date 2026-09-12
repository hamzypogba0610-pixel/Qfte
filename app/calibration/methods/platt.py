# app/calibration/methods/platt.py
"""
Platt Scaling pour QFTE.

Calibration de la forme :
p_calibrated = sigmoid(a * logit(p_raw) + b)
"""

from __future__ import annotations

import numpy as np
from typing import Optional
from sklearn.linear_model import LogisticRegression


class PlattScaler:
    """
    Platt Scaling avec option de pondération temporelle.
    """

    def __init__(self, C: float = 1.0):
        self.C = C
        self.model: Optional[LogisticRegression] = None
        self.fitted = False

    def fit(
        self,
        p_raw: np.ndarray,
        y: np.ndarray,
        sample_weight: Optional[np.ndarray] = None,
    ) -> "PlattScaler":
        """
        Entraîne le calibrateur.

        Args:
            p_raw: Probabilités brutes du modèle.
            y: Labels réels (0 ou 1).
            sample_weight: Poids optionnels (ex: décroissance temporelle).
        """
        eps = 1e-6
        p_clipped = np.clip(p_raw, eps, 1 - eps)
        z = np.log(p_clipped / (1 - p_clipped)).reshape(-1, 1)

        self.model = LogisticRegression(C=self.C, solver="lbfgs", max_iter=2000)

        if sample_weight is not None:
            self.model.fit(z, y, sample_weight=sample_weight)
        else:
            self.model.fit(z, y)

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
            raise ValueError("PlattScaler must be fitted before use.")

        eps = 1e-6
        p_clipped = np.clip(p_raw, eps, 1 - eps)
        z = np.log(p_clipped / (1 - p_clipped)).reshape(-1, 1)

        return self.model.predict_proba(z)[:, 1]
