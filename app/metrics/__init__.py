# app/metrics/__init__.py
"""
Métriques pour QFTE.

Fournit :
- Log Loss
- Brier score
- Expected Calibration Error (ECE)
- Autres métriques de classification
"""

from .classification import log_loss, brier_score, expected_calibration_error

__all__: list[str] = [
    "log_loss",
    "brier_score",
    "expected_calibration_error",
]
