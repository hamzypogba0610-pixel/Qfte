# app/experiments/config.py
"""
Configuration d'expérience pour QFTE.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Optional


@dataclass
class ExperimentConfig:
    """
    Configuration d'une expérience.
    """

    # Modèle
    model_name: Literal["logistic", "naive_bayes"] = "logistic"
    model_kwargs: Optional[dict] = None

    # Calibration
    calibration_method: Literal[
        "platt", "isotonic", "beta", "temperature", "histogram",
        "ensemble", "adaptive", "none"
    ] = "platt"
    recalibrate: bool = True
    recalibration_period: int = 500
    drift_detection: bool = True
    buffer_size: int = 2000

    # Données
    test_size: float = 0.2
    random_state: int = 42
    normalize: bool = True

    # Métriques
    metrics: list[str] = None

    def __post_init__(self):
        if self.model_kwargs is None:
            self.model_kwargs = {}

        if self.metrics is None:
            self.metrics = ["log_loss", "brier", "ece"]
