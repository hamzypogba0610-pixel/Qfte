# app/calibration/metrics/mce.py
"""
Maximum Calibration Error (MCE) pour QFTE.

Ce module fournira :
- Calcul du MCE.
- Identification du bin le plus mal calibré.
"""

from __future__ import annotations

import numpy as np
from typing import Dict, Optional, Any


def maximum_calibration_error(
    y_true: np.ndarray,
    p_pred: np.ndarray,
    n_bins: int = 10,
) -> Dict[str, Any]:
    """
    Calcule le MCE et identifie le bin le plus mal calibré.

    Args:
        y_true: Vecteur des vrais labels (0 ou 1).
        p_pred: Vecteur des probabilités prédites.
        n_bins: Nombre de bins pour la calibration.

    Returns:
        Dict {
            "mce": float,
            "worst_bin": {
                "bin": int,
                "confidence": float,
                "accuracy": float,
                "difference": float
            } | None,
            "n_bins": int
        }.
    """
    bin_edges = np.linspace(0.0, 1.0, n_bins + 1)
    bin_indices = np.digitize(p_pred, bin_edges[1:-1], right=False)

    mce = 0.0
    worst_bin = None

    for bin_id in range(n_bins):
        mask = bin_indices == bin_id
        if not np.any(mask):
            continue

        mean_pred = np.mean(p_pred[mask])
        observed = np.mean(y_true[mask])
        diff = abs(observed - mean_pred)

        if diff > mce:
            mce = diff
            worst_bin = {
                "bin": bin_id,
                "confidence": float(mean_pred),
                "accuracy": float(observed),
                "difference": float(diff),
            }

    return {
        "mce": float(mce),
        "worst_bin": worst_bin,
        "n_bins": n_bins,
    }
