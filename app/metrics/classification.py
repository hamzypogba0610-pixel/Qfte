# app/metrics/classification.py
"""
Métriques de classification pour QFTE.
"""

from __future__ import annotations

import numpy as np
from typing import Optional


def log_loss(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    eps: float = 1e-15,
) -> float:
    """
    Log Loss (perte logarithmique).

    Args:
        y_true: Labels réels (0 ou 1).
        y_pred: Probabilités prédites.
        eps: Terme de régularisation.

    Returns:
        Log Loss moyen.
    """
    y_pred = np.clip(y_pred, eps, 1 - eps)
    return float(
        -np.mean(
            y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred)
        )
    )


def brier_score(
    y_true: np.ndarray,
    y_pred: np.ndarray,
) -> float:
    """
    Brier Score (erreur quadratique moyenne).

    Args:
        y_true: Labels réels (0 ou 1).
        y_pred: Probabilités prédites.

    Returns:
        Brier Score moyen.
    """
    return float(np.mean((y_true - y_pred) ** 2))


def expected_calibration_error(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    n_bins: int = 10,
) -> float:
    """
    Expected Calibration Error (ECE).

    Args:
        y_true: Labels réels (0 ou 1).
        y_pred: Probabilités prédites.
        n_bins: Nombre de bins pour l'histogramme.

    Returns:
        ECE.
    """
    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    ece = 0.0

    for i in range(n_bins):
        in_bin = (y_pred > bin_boundaries[i]) & (y_pred <= bin_boundaries[i + 1])
        prop_in_bin = np.mean(in_bin)

        if prop_in_bin > 0:
            avg_confidence = np.mean(y_pred[in_bin])
            avg_accuracy = np.mean(y_true[in_bin])
            ece += np.abs(avg_accuracy - avg_confidence) * prop_in_bin

    return float(ece)
