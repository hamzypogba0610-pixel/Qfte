# app/experiments/train.py
"""
Entraînement et évaluation d'expériences.
"""

from __future__ import annotations

import numpy as np
from typing import Any, Dict
from .config import ExperimentConfig

from app.models import LogisticRegression, GaussianNaiveBayes
from app.calibration import CalibrationManager
from app.data import train_test_split, StandardScaler
from app.metrics import log_loss, brier_score, expected_calibration_error


def create_model(config: ExperimentConfig) -> Any:
    """Crée le modèle selon la config."""
    if config.model_name == "logistic":
        return LogisticRegression(**config.model_kwargs)
    elif config.model_name == "naive_bayes":
        return GaussianNaiveBayes(**config.model_kwargs)
    else:
        raise ValueError(f"Unknown model: {config.model_name}")


def run_experiment(
    X: np.ndarray,
    y: np.ndarray,
    config: ExperimentConfig,
) -> Dict[str, float]:
    """
    Lance une expérience.

    Args:
        X: Features.
        y: Labels.
        config: Configuration.

    Returns:
        Dict de métriques.
    """
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=config.test_size,
        random_state=config.random_state,
    )

    # Normalisation
    if config.normalize:
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

    # Modèle
    model = create_model(config)
    model.fit(X_train, y_train)

    # Prédictions brutes
    p_raw = model.predict_proba(X_test)

    # Calibration
    if config.calibration_method != "none":
        manager = CalibrationManager(
            method=config.calibration_method,
            recalibrate=config.recalibrate,
            recalibration_period=config.recalibration_period,
            drift_detection=config.drift_detection,
            buffer_size=config.buffer_size,
        )
        manager.fit(p_raw, y_test)
        p_calibrated = manager.predict(p_raw)
    else:
        p_calibrated = p_raw

    # Métriques
    metrics = {}

    if "log_loss" in config.metrics:
        metrics["log_loss"] = log_loss(y_test, p_calibrated)

    if "brier" in config.metrics:
        metrics["brier"] = brier_score(y_test, p_calibrated)

    if "ece" in config.metrics:
        metrics["ece"] = expected_calibration_error(y_test, p_calibrated)

    return metrics
