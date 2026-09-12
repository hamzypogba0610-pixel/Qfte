# app/calibration/hybrid/ensemble_calibration.py
"""
Ensemble de calibrateurs pour QFTE.

Combine plusieurs calibrateurs (Platt, Isotonic, Beta, etc.)
avec des poids optimisés pour minimiser le Log Loss.
"""

from __future__ import annotations

import numpy as np
from typing import Dict, List, Optional, Any
from scipy.optimize import minimize


class EnsembleCalibrator:
    """
    Ensemble de calibrateurs.
    """

    def __init__(self, calibrator_names: Optional[List[str]] = None):
        self.calibrator_names = calibrator_names or ["platt", "isotonic", "beta"]
        self.models: Dict[str, Any] = {}
        self.weights: Dict[str, float] = {}
        self.fitted = False

    def fit(
        self,
        p_raw: np.ndarray,
        y: np.ndarray,
        sample_weight: Optional[np.ndarray] = None,
    ) -> "EnsembleCalibrator":
        """
        Entraîne l'ensemble de calibrateurs.

        Args:
            p_raw: Probabilités brutes.
            y: Labels réels (0 ou 1).
            sample_weight: Poids optionnels.
        """
        from ..methods.platt import PlattScaler
        from ..methods.isotonic import IsotonicScaler
        from ..methods.beta import BetaCalibrator

        calibrator_classes = {
            "platt": PlattScaler,
            "isotonic": IsotonicScaler,
            "beta": BetaCalibrator,
        }

        # Entraîner chaque calibrateur
        for name in self.calibrator_names:
            if name not in calibrator_classes:
                continue
            cls = calibrator_classes[name]
            model = cls()
            model.fit(p_raw, y, sample_weight=sample_weight)
            self.models[name] = model

        # Calculer les poids optimaux
        self._compute_weights(p_raw, y)

        self.fitted = True
        return self

    def _compute_weights(
        self,
        p_raw: np.ndarray,
        y: np.ndarray,
    ) -> None:
        """
        Calcule les poids optimaux des calibrateurs.
        """
        if not self.models:
            return

        # Prédictions de chaque calibrateur
        predictions: Dict[str, np.ndarray] = {}
        for name, model in self.models.items():
            predictions[name] = model.predict(p_raw)

        def objective(weights):
            weights = weights / np.sum(weights)
            ensemble_pred = np.zeros(len(y))
            for i, name in enumerate(self.models.keys()):
                ensemble_pred += weights[i] * predictions[name]

            eps = 1e-15
            loss = -np.mean(
                y * np.log(ensemble_pred + eps)
                + (1 - y) * np.log(1 - ensemble_pred + eps)
            )
            return loss

        n_models = len(self.models)
        result = minimize(
            objective,
            np.ones(n_models) / n_models,
            method="SLSQP",
            bounds=[(0, 1)] * n_models,
            constraints={"type": "eq", "fun": lambda w: np.sum(w) - 1},
        )

        for i, name in enumerate(self.models.keys()):
            self.weights[name] = float(result.x[i])

    def predict(self, p_raw: np.ndarray) -> np.ndarray:
        """
        Calibration par ensemble.

        Args:
            p_raw: Probabilités brutes.

        Returns:
            Probabilités calibrées.
        """
        if not self.fitted:
            raise ValueError("EnsembleCalibrator must be fitted before use.")

        ensemble_pred = np.zeros(len(p_raw))
        for name, model in self.models.items():
            ensemble_pred += self.weights[name] * model.predict(p_raw)

        return ensemble_pred
