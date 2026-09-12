# app/models/logistic.py
"""
Régression logistique pour QFTE.
"""

from __future__ import annotations

import numpy as np
from typing import Optional
from .base import BaseModel


class LogisticRegression(BaseModel):
    """
    Régression logistique binaire.
    """

    def __init__(
        self,
        lr: float = 0.1,
        n_epochs: int = 100,
        fit_intercept: bool = True,
    ):
        self.lr = lr
        self.n_epochs = n_epochs
        self.fit_intercept = fit_intercept

        self.weights: Optional[np.ndarray] = None
        self.bias: float = 0.0

    def fit(
        self,
        X: np.ndarray,
        y: np.ndarray,
        sample_weight: Optional[np.ndarray] = None,
    ) -> "LogisticRegression":
        """
        Entraîne la régression logistique.

        Args:
            X: Features (n_samples, n_features).
            y: Labels (0 ou 1).
            sample_weight: Poids optionnels.
        """
        n_samples, n_features = X.shape

        # Initialisation
        self.weights = np.zeros(n_features)
        self.bias = 0.0

        # Ajout de l'intercept si demandé
        if self.fit_intercept:
            X_aug = np.hstack([X, np.ones((n_samples, 1))])
            self.weights = np.zeros(n_features + 1)
        else:
            X_aug = X

        # Pondération
        if sample_weight is None:
            sample_weight = np.ones(n_samples)
        sample_weight = sample_weight / np.mean(sample_weight)

        # Gradient descent
        for _ in range(self.n_epochs):
            logits = X_aug @ self.weights
            p_pred = 1 / (1 + np.exp(-logits))

            error = (p_pred - y) * sample_weight
            grad = (X_aug.T @ error) / n_samples

            self.weights -= self.lr * grad

        if self.fit_intercept:
            self.bias = float(self.weights[-1])
            self.weights = self.weights[:-1]

        self.fitted = True
        return self

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """
        Prédit les probabilités.

        Args:
            X: Features.

        Returns:
            Probabilités (classe 1).
        """
        if not self.fitted:
            raise ValueError("Model must be fitted before use.")

        if self.fit_intercept:
            X_aug = np.hstack([X, np.ones((X.shape, 1))])
            weights_aug = np.append(self.weights, self.bias)
        else:
            X_aug = X
            weights_aug = self.weights

        logits = X_aug @ weights_aug
        return 1 / (1 + np.exp(-logits))

    def predict(self, X: np.ndarray, threshold: float = 0.5) -> np.ndarray:
        """
        Prédit les labels.

        Args:
            X: Features.
            threshold: Seuil de décision.

        Returns:
            Labels prédits (0 ou 1).
        """
        p_pred = self.predict_proba(X)
        return (p_pred >= threshold).astype(int)
