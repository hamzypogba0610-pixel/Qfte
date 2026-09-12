# app/calibration/__init__.py
"""
Module de calibration pour QFTE.

Fournit des méthodes de calibration des probabilités :
- Platt scaling
- Isotonic regression
- Beta calibration
- Calibration hybride (ensemble, adaptative, en ligne)
- Gestion de la recalibration (drift detection, stratégies)
"""

from .methods.platt import PlattScaler
from .methods.isotonic import IsotonicScaler
from .methods.beta import BetaCalibrator
from .methods.temperature_scaling import TemperatureScaling
from .methods.histogram import HistogramCalibrator

from .hybrid.ensemble_calibration import EnsembleCalibrator
from .hybrid.adaptive_calibration import AdaptiveCalibrator

from .recalibration.drift_detection import DriftDetector
from .recalibration.recalibration_strategy import (
    RecalibrationStrategy,
    PeriodicStrategy,
    DriftBasedStrategy,
    HybridStrategy,
)
from .recalibration.recalibration_manager import RecalibrationManager

from .manager import CalibrationManager

__all__: list[str] = [
    # Méthodes de base
    "PlattScaler",
    "IsotonicScaler",
    "BetaCalibrator",
    "TemperatureScaling",
    "HistogramCalibrator",
    # Calibration hybride
    "EnsembleCalibrator",
    "AdaptiveCalibrator",
    # Recalibration
    "DriftDetector",
    "RecalibrationStrategy",
    "PeriodicStrategy",
    "DriftBasedStrategy",
    "HybridStrategy",
    "RecalibrationManager",
    # Manager principal
    "CalibrationManager",
]
