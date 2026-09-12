# app/analysis/types.py
"""
Structures de données pour les analyses QFTE (match, marchés, etc.).
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class MarketPrediction:
    """
    Prédiction pour un marché donné (1N2, OU, handicap, BTTS, score, etc.).
    """
    market_type: str          # "1N2", "OU_1.5", "OU_2.5", "OU_3.5", "handicap", "btts", "score_ht", "score_ft"
    recommendation: str       # ex: "1", "N", "2", "Over", "Under", "BTTS_Oui", "BTTS_Non", "1-0", etc.
    confidence: float         # 0–10
    proba: Optional[float] = None  # proba calibrée principale (ex: proba de la recommandation)
    details: Dict[str, float] = field(default_factory=dict)  # probas détaillées (ex: {"1": 0.58, "N": 0.24, "2": 0.18})

    def __post_init__(self):
        if not (0.0 <= self.confidence <= 10.0):
            raise ValueError("confidence doit être entre 0 et 10")


@dataclass
class MatchAnalysis:
    """
    Analyse complète d'un match (pré-live ou live).
    """
    sport: str                # "football", "basketball", "tennis"
    competition: str
    home: str
    away: str
    start_time: str           # ex: "2026-09-15T21:00:00"
    is_live: bool             # False = pré-live, True = live
    score_current: Optional[str] = None  # ex: "1-0", "45-42", "1-1 (sets)"
    minute: Optional[str] = None         # ex: "32'", "Q2", "Set 2"

    # Prédictions par marché
    winner: Optional[MarketPrediction] = None
    ou_1_5: Optional[MarketPrediction] = None
    ou_2_5: Optional[MarketPrediction] = None
    ou_3_5: Optional[MarketPrediction] = None
    handicap: Optional[MarketPrediction] = None
    btts: Optional[MarketPrediction] = None      # None si sport non concerné
    score_ht: Optional[MarketPrediction] = None  # None si non pertinent
    score_ft: Optional[MarketPrediction] = None

    # Métriques globales
    global_confidence: float = 0.0   # 0–10
    edge: float = 0.0                # edge principal (ex: sur la recommandation globale)
    strong_markets_count: int = 0    # nombre de marchés avec confiance ≥ 7.5

    def __post_init__(self):
        if not (0.0 <= self.global_confidence <= 10.0):
            raise ValueError("global_confidence doit être entre 0 et 10")
        if self.strong_markets_count < 0:
            raise ValueError("strong_markets_count doit être >= 0")
