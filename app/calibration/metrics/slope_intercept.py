# app/calibration/metrics/slope_intercept.py
"""
Calibration slope & intercept pour QFTE.

On ajuste : logit(Y) = α + β * logit(p)
Idéalement : α = 0, β = 1.
"""

from __future__ import annotations

import numpy as np
from typing import Dict, Any, Optional


def calibration_slope_intercept(
    y_true: np.ndarray,
    p_pred: np.ndarray,
    eps: float = 1e-6,
    random_state: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Calcule la slope et l'intercept de calibration avec intervalles de confiance (bootstrap).

    Args:
        y_true: Vecteur des vrais labels (0 ou 1).
        p_pred: Vecteur des probabilités prédites.
        eps: Terme de lissage pour éviter log(0).
        random_state: Graine aléatoire.

    Returns:
        Dict {
            "slope": float,
            "slope_ci": (float, float),
            "intercept": float,
            "intercept_ci": (float, float),
            "interpretation": {
                "slope": str,
                "intercept": str
            }
        }.
    """
    rng = np.random.default_rng(random_state)

    # Log-odds
    p_clipped = np.clip(p_pred, eps, 1 - eps)
    z = np.log(p_clipped / (1 - p_clipped)).reshape(-1, 1)

    # Régression logistique simple (slope & intercept)
    slope, intercept = _fit_logistic(z, y_true)

    # Bootstrap pour les intervalles de confiance
    n = len(y_true)
    slopes = []
    intercepts = []

    for _ in range(1000):
        indices = rng.choice(n, n, replace=True)
        try:
            s, i = _fit_logistic(z[indices], y_true[indices])
            slopes.append(s)
            intercepts.append(i)
        except Exception:
            continue

    slope_ci = (
        float(np.percentile(slopes, 2.5)) if slopes else None,
        float(np.percentile(slopes, 97.5)) if slopes else None,
    )
    intercept_ci = (
        float(np.percentile(intercepts, 2.5)) if intercepts else None,
        float(np.percentile(intercepts, 97.5)) if intercepts else None,
    )

    # Interprétation
    slope_interp = (
        "Good"
        if 0.9 <= slope <= 1.1
        else ("Too extreme" if slope < 0.9 else "Too conservative")
    )
    intercept_interp = "Good" if abs(intercept) < 0.1 else "Biased"

    return {
        "slope": float(slope),
        "slope_ci": slope_ci,
        "intercept": float(intercept),
        "intercept_ci": intercept_ci,
        "interpretation": {
            "slope": slope_interp,
            "intercept": intercept_interp,
        },
    }


def _fit_logistic(z: np.ndarray, y: np.ndarray):
    """
    Ajuste une régression logistique simple (1 feature).
    Retourne (slope, intercept).
    """
    from sklearn.linear_model import LogisticRegression

    model = LogisticRegression(solver="lbfgs", max_iter=2000)
    model.fit(z, y)

    slope = float(model.coef_[0, 0])
    intercept = float(model.intercept_)

    return slope, intercept
