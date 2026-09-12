# app/calibration/methods/isotonic.py
"""
Isotonic Regression pour QFTE.

Calibration non paramétrique, monotone.
"""

from __future__ import annotations

import numpy as np
from typing import Optional
from sklearn.isotonic import IsotonicRegression


class IsotonicScaler:
    """
    Isotonic Regression avec option de pondération temporelle.
    """

    def __init__(self):
        self.model: Optional[IsotonicRegression] = None
        self.fitted = False

    def fit(
        self,
        p_raw: np.ndarray,
        y: np.ndarray,
        sample_weight: Optional[np.ndarray] = None,
    ) -> "IsotonicScaler":
        """
        Entraîne le calibrateur.

        Args:
            p_raw: Probabilités brutes du modèle.
            y: Labels réels (0 ou 1).
            sample_weight: Poids optionnels (ex: décroissance temporelle).
        """
        self.model = IsotonicRegression(
            y_min=1e-4, y_max=1 - 1e-4, out_of_bounds="clip"
        )

        if sample_weight is not None:
            self.model.fit(p_raw, y, sample_weight=sample_weight)
        else:
            self.model.fit(p_raw, y)

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
            raise ValueError("IsotonicScaler must be fitted before use.")

        return np.asarray(self.model.predict(p_raw), dtype=float)
