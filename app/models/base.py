# app/models/base.py
"""
Classe de base pour les modèles de QFTE.
"""

from __future__ import annotations

import numpy as np
from abc import ABC, abstractmethod
from typing import Any, Optional


class BaseModel(ABC):
    """
    Interface de base pour un modèle.
    """

    def __init__(self):
        self.fitted = False

    @abstractmethod
    def fit(
        self,
        X: np.ndarray,
        y: np.ndarray,
        sample_weight: Optional[np.ndarray] = None,
    ) -> "BaseModel":
        """Entraîne le modèle."""
        pass

    @abstractmethod
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Prédictions (labels ou probabilités)."""
        pass

    def save(self, filepath: str) -> None:
        """Sauvegarde le modèle."""
        import pickle
        from pathlib import Path

        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load(filepath: str) -> "BaseModel":
        """Charge un modèle sauvegardé."""
        import pickle

        with open(filepath, "rb") as f:
            return pickle.load(f)
