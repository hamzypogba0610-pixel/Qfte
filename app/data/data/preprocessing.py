# app/data/preprocessing.py
"""
Préprocessing pour QFTE.
"""

from __future__ import annotations

import numpy as np
from typing import Tuple


def train_test_split(
    X: np.ndarray,
    y: np.ndarray,
    test_size: float = 0.2,
    random_state: Optional[int] = None,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Sépare les données en train / test.

    Args:
        X: Features.
        y: Target.
        test_size: Proportion pour le test.
        random_state: Graine aléatoire.

    Returns:
        X_train, X_test, y_train, y_test.
    """
    n_samples = len(y)
    indices = np.arange(n_samples)

    if random_state is not None:
        np.random.seed(random_state)

    np.random.shuffle(indices)

    n_test = int(test_size * n_samples)
    test_indices = indices[:n_test]
    train_indices = indices[n_test:]

    return (
        X[train_indices],
        X[test_indices],
        y[train_indices],
        y[test_indices],
    )


class StandardScaler:
    """
    Normalisation standard (moyenne 0, écart-type 1).
    """

    def __init__(self):
        self.mean_: np.ndarray | None = None
        self.std_: np.ndarray | None = None
        self.fitted = False

    def fit(self, X: np.ndarray) -> "StandardScaler":
        """
        Calcule moyenne et écart-type.

        Args:
            X: Features (n_samples, n_features).
        """
        self.mean_ = np.mean(X, axis=0)
        self.std_ = np.std(X, axis=0) + 1e-10
        self.fitted = True
        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        """
        Normalise les données.

        Args:
            X: Features.

        Returns:
            Données normalisées.
        """
        if not self.fitted:
            raise ValueError("StandardScaler must be fitted before use.")

        return (X - self.mean_) / self.std_

    def fit_transform(self, X: np.ndarray) -> np.ndarray:
        """Fit + transform."""
        self.fit(X)
        return self.transform(X)
