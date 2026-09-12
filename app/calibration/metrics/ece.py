# app/calibration/metrics/ece.py
"""
Expected Calibration Error (ECE) avancé pour QFTE.

Ce module fournira :
- ECE avec intervalles de confiance (bootstrap).
- Support pour bins uniformes ou par quantiles.
"""

from __future__ import annotations

import numpy as np
from typing import Dict, Tuple, Optional


def expected_calibration_error(
    y_true: np.ndarray,
    p_pred: np.ndarray,
    n_bins: int = 10,
    strategy: str = "quantile",
    n_bootstrap: int = 1000,
    confidence: float = 0.95,
    random_state: Optional[int] = None,
) -> Dict:
    """
    Calcule l'ECE avec intervalles de confiance par bootstrap.

    Args:
        y_true: Vecteur des vrais labels (0 ou 1).
        p_pred: Vecteur des probabilités prédites.
        n_bins: Nombre de bins pour la calibration.
        strategy: "uniform" ou "quantile".
        n_bootstrap: Nombre de tirages bootstrap.
        confidence: Niveau de confiance pour l'intervalle.
        random_state: Graine aléatoire.

    Returns:
        Dict {
            "ece": float,
            "ci_lower": float,
            "ci_upper": float,
            "n_bins": int,
            "strategy": str
        }.
    """
    rng = np.random.default_rng(random_state)

    # Calcul de l'ECE
    ece = _compute_ece(y_true, p_pred, n_bins, strategy)

    # Bootstrap pour l'intervalle de confiance
    ece_values = []
    n = len(y_true)

    for _ in range(n_bootstrap):
        indices = rng.choice(n, n, replace=True)
        ece_boot = _compute_ece(y_true[indices], p_pred[indices], n_bins, strategy)
        ece_values.append(ece_boot)

    ci_lower = np.percentile(ece_values, (1 - confidence) / 2 * 100)
    ci_upper = np.percentile(ece_values, (1 + confidence) / 2 * 100)

    return {
        "ece": ece,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "n_bins": n_bins,
        "strategy": strategy,
    }


def _compute_ece(
    y_true: np.ndarray,
    p_pred: np.ndarray,
    n_bins: int,
    strategy: str,
) -> float:
    """
    Calcule l'ECE (sans bootstrap).
    """
    if strategy == "uniform":
        bin_edges = np.linspace(0.0, 1.0, n_bins + 1)
    else:  # quantile
        bin_edges = np.unique(np.quantile(p_pred, np.linspace(0, 1, n_bins + 1)))

    bin_indices = np.digitize(p_pred, bin_edges[1:-1], right=False)

    ece = 0.0
    n = len(y_true)

    for bin_id in range(len(bin_edges) - 1):
        mask = bin_indices == bin_id
        if not np.any(mask):
            continue

        mean_pred = np.mean(p_pred[mask])
        observed = np.mean(y_true[mask])
        weight = np.sum(mask) / n

        ece += weight * abs(observed - mean_pred)

    return ece
