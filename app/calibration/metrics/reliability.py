# app/calibration/metrics/reliability.py
"""
Courbe de fiabilité pour QFTE.

Ce module fournira :
- Calcul de la courbe de fiabilité avec intervalles de confiance (Wilson).
- Fonction utilitaire pour tracer la courbe (plus tard, dans un notebook ou dashboard).
"""

from __future__ import annotations

import numpy as np
from scipy.stats import norm
from typing import Dict, List, Any


def compute_reliability_curve(
    y_true: np.ndarray,
    p_pred: np.ndarray,
    n_bins: int = 10,
    strategy: str = "quantile",
) -> Dict[str, Any]:
    """
    Calcule la courbe de fiabilité avec intervalles de confiance (Wilson).

    Args:
        y_true: Vecteur des vrais labels (0 ou 1).
        p_pred: Vecteur des probabilités prédites.
        n_bins: Nombre de bins.
        strategy: "uniform" ou "quantile".

    Returns:
        Dict {
            "bin_centers": List[float],
            "observed_frequencies": List[float],
            "confidences": List[float],
            "counts": List[int],
            "ci_lower": List[float],
            "ci_upper": List[float]
        }.
    """
    if strategy == "uniform":
        bin_edges = np.linspace(0.0, 1.0, n_bins + 1)
    else:
        bin_edges = np.unique(np.quantile(p_pred, np.linspace(0, 1, n_bins + 1)))

    bin_indices = np.digitize(p_pred, bin_edges[1:-1], right=False)

    bin_centers: List[float] = []
    observed_frequencies: List[float] = []
    confidences: List[float] = []
    counts: List[int] = []
    ci_lower: List[float] = []
    ci_upper: List[float] = []

    for bin_id in range(len(bin_edges) - 1):
        mask = bin_indices == bin_id
        if not np.any(mask):
            continue

        n = np.sum(mask)
        mean_pred = float(np.mean(p_pred[mask]))
        observed = float(np.mean(y_true[mask]))

        # Intervalle de Wilson
        z = norm.ppf(0.975)
        denominator = 1 + z**2 / n
        center = observed + z**2 / (2 * n)
        radius = z * np.sqrt(
            observed * (1 - observed) / n + z**2 / (4 * n**2)
        )
        lower = max(0.0, float((center - radius) / denominator))
        upper = min(1.0, float((center + radius) / denominator))

        bin_centers.append(mean_pred)
        observed_frequencies.append(observed)
        confidences.append(mean_pred)
        counts.append(int(n))
        ci_lower.append(lower)
        ci_upper.append(upper)

    return {
        "bin_centers": bin_centers,
        "observed_frequencies": observed_frequencies,
        "confidences": confidences,
        "counts": counts,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
    }
