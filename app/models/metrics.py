# app/models/metrics.py
"""
Métriques d'évaluation des prédictions probabilistes.

Ce module fournit :
- Brier score
- Log Loss
- ECE (Expected Calibration Error)
"""

from __future__ import annotations

from typing import Dict, List, Tuple

import numpy as np


def brier_score(
    probs: List[Dict[str, float]],
    outcomes: List[str],
) -> float:
    """
    Calcule le Brier score pour des prédictions 1X2.

    Args:
        probs: Liste de dicts {"1": p1, "X": pX, "2": p2}.
        outcomes: Liste de résultats réels ("1", "X", "2").

    Returns:
        Brier score moyen.
    """
    # Squelette : à implémenter plus tard
    raise NotImplementedError


def log_loss(
    probs: List[Dict[str, float]],
    outcomes: List[str],
) -> float:
    """
    Calcule le Log Loss pour des prédictions 1X2.

    Args:
        probs: Liste de dicts {"1": p1, "X": pX, "2": p2}.
        outcomes: Liste de résultats réels ("1", "X", "2").

    Returns:
        Log Loss moyen.
    """
    # Squelette : à implémenter plus tard
    raise NotImplementedError


def ece(
    probs: List[Dict[str, float]],
    outcomes: List[str],
    n_bins: int = 10,
) -> float:
    """
    Calcule l'Expected Calibration Error (ECE).

    Args:
        probs: Liste de dicts {"1": p1, "X": pX, "2": p2}.
        outcomes: Liste de résultats réels ("1", "X", "2").
        n_bins: Nombre de bins pour la calibration.

    Returns:
        ECE.
    """
    # Squelette : à implémenter plus tard
    raise NotImplementedError
