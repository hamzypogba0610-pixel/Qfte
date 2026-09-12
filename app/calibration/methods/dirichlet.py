# app/calibration/methods/dirichlet.py
"""
Dirichlet Calibration pour QFTE.

Calibration pour modèles multiclasses (ex: 1, X, 2).
Conserve la somme des probabilités égale à 1.
"""

from __future__ import annotations

import numpy as np
from typing import Optional


class DirichletCalibrator:
    """
    Dirichlet Calibration (version simplifiée, à enrichir plus tard).
    """

    def __init__(self):
        self.W: Optional[np.ndarray] = None
        self.b: Optional[np.ndarray] = None
        self.fitted = False

    def fit(self, p_raw: np.ndarray, y: np.ndarray) -> "DirichletCalibrator":
        """
        Entraîne le calibrateur.

        Args:
            p_raw: Matrice de probabilités brutes (n_samples, n_classes).
            y: Matrice one-hot des labels réels (n_samples, n_classes).
        """
        # Version simplifiée : identité (à améliorer plus tard)
        n_classes = p_raw.shape[1]
        self.W = np.eye(n_classes)
        self.b = np.zeros(n_classes)
        self.fitted = True
        return self

    def predict(self, p_raw: np.ndarray) -> np.ndarray:
        """
        Calibre de nouvelles probabilités.

        Args:
            p_raw: Matrice de probabilités brutes (n_samples, n_classes).

        Returns:
            Matrice de probabilités calibrées (n_samples, n_classes).
        """
        if not self.fitted:
            raise ValueError("DirichletCalibrator must be fitted before use.")

        logits = np.log(p_raw + 1e-6)
        transformed = logits @ self.W + self.b
        exp_t = np.exp(transformed)
        return exp_t / np.sum(exp_t, axis=1, keepdims=True)
