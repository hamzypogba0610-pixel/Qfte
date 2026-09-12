# app/calibration/metrics/log_loss.py
"""
Log Loss pour QFTE.

Métrique de calibration qui pénalise fortement
les probabilités extrêmement confiantes mais fausses.
"""

from __future__ import annotations

import numpy as np
from typing import Dict


def log_loss(
    y_true: np.ndarray,
    p_pred: np.ndarray,
    eps: float = 1e-15,
) -> Dict:
    """
    Calcule le Log Loss.

    Args:
        y_true: Vecteur des vrais labels (0 ou 1).
        p_pred: Vecteur des probabilités prédites.
        eps: Terme de lissage pour éviter log(0).

    Returns:
        Dict {
            "log_loss": float,
            "n_samples": int
        }.
    """
    p_clipped = np.clip(p_pred, eps, 1 - eps)

    ll = -np.mean(
        y_true * np.log(p_clipped) + (1 - y_true) * np.log(1 - p_clipped)
    )

    return {
        "log_loss": float(ll),
        "n_samples": int(len(y_true)),
    }
