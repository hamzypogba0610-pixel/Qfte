# app/models/naive_bayes.py
"""
Naive Bayes binaire pour QFTE.
"""

from __future__ import annotations

import numpy as np
from typing import Optional
from .base import BaseModel


class GaussianNaiveBayes(BaseModel):
    """
    Naive Bayes gaussien pour classification binaire.
    """

    def __init__(self, var_smoothing: float = 1e-9):
        self.var_smoothing = var_smoothing
        self.classes_: Optional[np.ndarray] = None
        self.theta_: np.ndarray | None = None  # moyennes par classe
        self.var_: np.ndarray | None = None    # variances par classe
        self.class_prior_: np.ndarray | None = None

    def fit(
        self,
        X: np.ndarray,
        y: np.ndarray,
        sample_weight: Optional[np.ndarray] = None,
    ) -> "GaussianNaiveBayes":
        """
        Entraîne le modèle.

        Args:
            X: Features (n_samples, n_features).
            y: Labels (0 ou 1).
            sample_weight: Poids optionnels.
        """
        n_samples, n_features = X.shape
        self.classes_ = np.array([0, 1])

        if sample_weight is None:
            sample_weight = np.ones(n_samples)
        sample_weight = sample_weight / np.sum(sample_weight)

        self.theta_ = np.zeros((2, n_features))
        self.var_ = np.zeros((2, n_features))
        self.class_prior_ = np.zeros(2)

        for c in [0, 1]:
            X_c = X[y == c]
            w_c = sample_weight[y == c]
            w_c = w_c / np.sum(w_c)

            self.theta_[c] = np.sum(X_c * w_c[:, None], axis=0)
            self.var_[c] = np.sum(
                ((X_c - self.theta_[c]) ** 2) * w_c[:, None], axis=0
            ) + self.var_smoothing

            self.class_prior_[c] = np.sum(sample_weight[y == c])

        self.fitted = True
        return self

    def _joint_log_likelihood(self, X: np.ndarray) -> np.ndarray:
        """Calcule le log de la vraisemblance jointe par classe."""
        joint_log_like = np.zeros((X.shape, 2))

        for c in [0, 1]:
            joint_log_like[:, c] = (
                np.log(self.class_prior_[c])
                - 0.5 * np.sum(np.log(2.0 * np.pi * self.var_[c]))
                - 0.5 * np.sum((X - self.theta_[c]) ** 2 / self.var_[c], axis=1)
            )

        return joint_log_like

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

        joint_log_like = self._joint_log_likelihood(X)

        # Normalisation pour avoir des probas
        log_sum_exp = np.max(joint_log_like, axis=1, keepdims=True)
        log_probs = joint_log_like - log_sum_exp
        probs = np.exp(log_probs)
        probs = probs / np.sum(probs, axis=1, keepdims=True)

        return probs[:, 1]

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
