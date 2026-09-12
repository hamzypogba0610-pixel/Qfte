# app/calibration/metrics/brier.py
"""
Brier Score décomposé pour QFTE.

Décomposition :
BS = Incertitude - Résolution + Fiabilité
"""

from __future__ import annotations

import numpy as np
from typing import Dict


def brier_decomposition(
    y_true: np.ndarray,
    p_pred: np.ndarray,
    n_bins: int = 10,
) -> Dict:
    """
    Décompose le Brier Score en incertitude, résolution et fiabilité.

    Args:
        y_true: Vecteur des vrais labels (0 ou 1).
        p_pred: Vecteur des probabilités prédites.
        n_bins: Nombre de bins pour la calibration.

    Returns:
        Dict {
            "brier_score": float,
            "uncertainty": float,
            "resolution": float,
            "reliability": float,
            "check": float  # uncertainty - resolution + reliability
        }.
    """
    # Brier Score
    bs = float(np.mean((p_pred - y_true) ** 2))

    # Incertitude
    base_rate = float(np.mean(y_true))
    uncertainty = base_rate * (1 - base_rate)

    # Résolution et Fiabilité
    bin_edges = np.linspace(0.0, 1.0, n_bins + 1)
    bin_indices = np.digitize(p_pred, bin_edges[1:-1], right=False)

    reliability = 0.0
    resolution = 0.0
    n = len(y_true)

    for bin_id in range(n_bins):
        mask = bin_indices == bin_id
        if not np.any(mask):
            continue

        mean_pred = np.mean(p_pred[mask])
        observed = np.mean(y_true[mask])
        weight = np.sum(mask) / n

        reliability += weight * (observed - mean_pred) ** 2
        resolution += weight * (observed - base_rate) ** 2

    return {
        "brier_score": bs,
        "uncertainty": uncertainty,
        "resolution": float(resolution),
        "reliability": float(reliability),
        "check": uncertainty - resolution + reliability,
    }
