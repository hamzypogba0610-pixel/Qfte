# app/utils/validation.py
"""
Validation des inputs pour QFTE.
"""

from __future__ import annotations

import numpy as np
from typing import Tuple


def validate_proba(
    p: np.ndarray,
    eps: float = 1e-15,
) -> np.ndarray:
    """
    Valide et nettoie un tableau de probabilités.

    Args:
        p: Tableau de probabilités.
        eps: Terme de régularisation.

    Returns:
        Tableau de probabilités validé.
    """
    p = np.asarray(p, dtype=float)

    if p.ndim != 1:
        raise ValueError("p must be a 1D array.")

    if np.any((p < 0) | (p > 1)):
        raise ValueError("Probabilities must be in [0, 1].")

    # Clip pour éviter 0 et 1
    return np.clip(p, eps, 1 - eps)


def validate_labels(y: np.ndarray) -> np.ndarray:
    """
    Valide un tableau de labels binaires.

    Args:
        y: Tableau de labels.

    Returns:
        Tableau de labels validé (0 ou 1).
    """
    y = np.asarray(y, dtype=float)

    if y.ndim != 1:
        raise ValueError("y must be a 1D array.")

    unique = np.unique(y)
    if not np.all(np.isin(unique, [0, 1])):
        raise ValueError("Labels must be 0 or 1.")

    return y.astype(int)
