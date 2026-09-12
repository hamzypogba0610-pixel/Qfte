# app/analysis/__init__.py
"""
Module d'analyse QFTE : prédiction de matchs, sélection des meilleures opportunités.
"""

from .types import MarketPrediction, MatchAnalysis
from . import config
from . import predictor
from . import selector

__all__ = [
    "MarketPrediction",
    "MatchAnalysis",
    "config",
    "predictor",
    "selector",
]
