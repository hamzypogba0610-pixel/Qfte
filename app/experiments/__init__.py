# app/experiments/__init__.py
"""
Expériences pour QFTE.

Fournit :
- Configurations d'entraînement.
- Scripts pour lancer des expériences.
"""

from .config import ExperimentConfig
from .train import run_experiment

__all__: list[str] = [
    "ExperimentConfig",
    "run_experiment",
]
