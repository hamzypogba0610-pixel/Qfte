# app/models/tree.py
"""
Arbre de décision très simple pour QFTE.
"""

from __future__ import annotations

import numpy as np
from typing import Optional, Dict, Any
from .base import BaseModel


class DecisionStump:
    """
    Noeud de décision (stump).
    """

    def __init__(self):
        self.feature_index: Optional[int] = None
        self.threshold: float = 0.0
        self.left_value: float = 0.0   # proba si feature <= threshold
        self.right_value: float = 0.0  # proba si feature > threshold
        self.is_leaf: bool = False
        self.leaf_value: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "feature_index": self.feature_index,
            "threshold": self.threshold,
            "left_value": self.left_value,
            "right_value": self.right_value,
            "is_leaf": self.is_leaf,
            "leaf_value": self.leaf_value,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "DecisionStump":
        stump = DecisionStump()
        stump.feature_index = d["feature_index"]
        stump.threshold = d["threshold"]
        stump.left_value = d["left_value"]
        stump.right_value = d["right_value"]
        stump.is_leaf = d["is_leaf"]
        stump.leaf_value = d["leaf_value"]
        return stump


class SimpleDecisionTree(BaseModel):
    """
    Arbre de décision simple (profondeur max = 2).
    """

    def __init__(
        self,
        max_depth: int = 2,
        min_samples_leaf: int = 10,
    ):
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.root: Optional[DecisionStump] = None
        self.left_child: Optional[DecisionStump] = None
        self.right_child: Optional[DecisionStump] = None

    def _gini(self, y: np.ndarray) -> float:
        if len(y) == 0:
            return 0.0
        p = np.mean(y)
        return float(2 * p * (1 - p))

    def _find_best_split(
        self,
        X: np.ndarray,
        y: np.ndarray,
    ):
        """Trouve le meilleur split (feature, threshold)."""
        n_samples, n_features = X.shape
        best_gini = float("inf")
        best_feature = 0
        best_threshold = 0.0

        parent_gini = self._gini(y)

        for feature_index in range(n_features):
            thresholds = np.unique(X[:, feature_index])
            if len(thresholds) > 20:
                thresholds = np.percentile(
                    X[:, feature_index], np.linspace(0, 100, 20)
                )

            for threshold in thresholds:
                left_mask = X[:, feature_index] <= threshold
                right_mask = ~left_mask

                if (
                    np.sum(left_mask) < self.min_samples_leaf
                    or np.sum(right_mask) < self.min_samples_leaf
                ):
                    continue

                left_gini = self._gini(y[left_mask])
                right_gini = self._gini(y[right_mask])

                n_left = np.sum(left_mask)
                n_right = np.sum(right_mask)

                weighted_gini = (
                    n_left * left_gini + n_right * right_gini
                ) / n_samples

                if weighted_gini < best_gini:
                    best_gini = weighted_gini
                    best_feature = feature_index
                    best_threshold = threshold

        return best_feature, best_threshold

    def fit(
        self,
        X: np.ndarray,
        y: np.ndarray,
        sample_weight: Optional[np.ndarray] = None,
    ) -> "SimpleDecisionTree":
        """
        Entraîne l'arbre (profondeur max 2).

        Args:
            X: Features (n_samples, n_features).
            y: Labels (0 ou 1).
            sample_weight: Non utilisé ici.
        """
        n_samples, n_features = X.shape

        # Racine
        self.root = DecisionStump()
        feature_index, threshold = self._find_best_split(X, y)

        self.root.feature_index = feature_index
        self.root.threshold = threshold

        left_mask = X[:, feature_index] <= threshold
        right_mask = ~left_mask

        # Valeurs des feuilles enfants
        left_proba = np.mean(y[left_mask]) if np.sum(left_mask) > 0 else 0.5
        right_proba = (
            np.mean(y[right_mask]) if np.sum(right_mask) > 0 else 0.5
        )

        # Si profondeur 1, on reste à un stump
        if self.max_depth == 1:
            self.root.is_leaf = True
            self.root.leaf_value = 0.5  # pas utilisé, mais cohérent
            self.root.left_value = left_proba
            self.root.right_value = right_proba
            self.fitted = True
            return self

        # Sinon, on crée deux enfants (stumps leaves)
        self.left_child = DecisionStump()
        self.left_child.is_leaf = True
        self.left_child.leaf_value = left_proba

        self.right_child = DecisionStump()
        self.right_child.is_leaf = True
        self.right_child.leaf_value = right_proba

        self.root.is_leaf = False
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
        if not self.fitted or self.root is None:
            raise ValueError("Model must be fitted before use.")

        n_samples = X.shape
        p_pred = np.zeros(n_samples)

        feature_index = self.root.feature_index
        threshold = self.root.threshold

        left_mask = X[:, feature_index] <= threshold
        right_mask = ~left_mask

        if self.root.is_leaf:
            # Un seul niveau
            p_pred[left_mask] = self.root.left_value
            p_pred[right_mask] = self.root.right_value
        else:
            # Deux niveaux
            p_pred[left_mask] = self.left_child.leaf_value
            p_pred[right_mask] = self.right_child.leaf_value

        return p_pred

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
