# app/engines/decision.py
"""
Decision Engine pour QFTE.

Ce module fournit :
- Les règles de décision : BET / WATCH / PASS.
- L'intégration de l'EV, du DRS (confiance data), et de la liquidité.
- Une fonction qui renvoie la décision finale pour un match.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional


class Decision(Enum):
    BET = "BET"       # Pari recommandé
    WATCH = "WATCH"   # À surveiller, pas de pari
    PASS = "PASS"     # Aucun intérêt / trop risqué


@dataclass
class DecisionContext:
    """
    Contexte nécessaire pour prendre une décision.
    """
    ev_max: float                # EV maximum parmi 1, X, 2
    best_outcome: str            # "1", "X" ou "2"
    drs_score: Optional[float]   # Score de confiance data (0..1)
    liquidity_score: Optional[float]  # Score de liquidité (0..1)
    edge_threshold: float = 0.05     # EV minimum pour considérer un bet
    drs_threshold: float = 0.6       # Confiance data minimum
    liquidity_threshold: float = 0.5 # Liquidité minimum


def decide_bet(
    ctx: DecisionContext,
) -> Decision:
    """
    Prend une décision BET / WATCH / PASS en fonction du contexte.

    Règles de base (à affiner plus tard) :
    - Si EV < edge_threshold → PASS
    - Si EV >= edge_threshold mais DRS ou liquidité trop faibles → WATCH
    - Si EV >= edge_threshold et DRS & liquidité OK → BET

    Args:
        ctx: DecisionContext avec EV, DRS, liquidité, seuils.

    Returns:
        Decision (BET, WATCH ou PASS).
    """
    # Squelette : à implémenter plus tard
    raise NotImplementedError


def build_decision_context(
    ev_by_outcome: Dict[str, float],
    drs_score: Optional[float] = None,
    liquidity_score: Optional[float] = None,
    edge_threshold: float = 0.05,
    drs_threshold: float = 0.6,
    liquidity_threshold: float = 0.5,
) -> DecisionContext:
    """
    Construit un DecisionContext à partir des EV et scores.

    Args:
        ev_by_outcome: Dict {"1": ev1, "X": evX, "2": ev2}.
        drs_score: Score de confiance data (0..1).
        liquidity_score: Score de liquidité (0..1).
        edge_threshold: EV minimum pour considérer un bet.
        drs_threshold: Confiance data minimum.
        liquidity_threshold: Liquidité minimum.

    Returns:
        DecisionContext prêt à être passé à decide_bet().
    """
    # Squelette : à implémenter plus tard
    raise NotImplementedError
