# app/engines/market.py
"""
Market Engine pour QFTE.

Ce module fournit :
- Le calcul des cotes implicites à partir des probabilités.
- Le calcul de l'EV (expected value) pour chaque issue (1, X, 2).
- Des utilitaires pour comparer probas modèle vs cotes bookmaker.
"""

from __future__ import annotations

from typing import Dict, List, Tuple


def implied_probs_from_odds(
    odds: Dict[str, float],
) -> Dict[str, float]:
    """
    Calcule les probabilités implicites à partir des cotes décimales.

    Args:
        odds: Dict {"1": odd1, "X": oddX, "2": odd2}.

    Returns:
        Dict {"1": p1, "X": pX, "2": p2} avec p = 1 / odd.
    """
    # Squelette : à implémenter plus tard
    raise NotImplementedError


def ev_for_outcome(
    model_prob: float,
    decimal_odd: float,
) -> float:
    """
    Calcule l'EV pour une issue donnée.

    EV = (model_prob * decimal_odd) - 1

    Args:
        model_prob: Probabilité estimée par le modèle (0..1).
        decimal_odd: Cote décimale offerte par le bookmaker.

    Returns:
        Expected value (EV). > 0 = bet +EV.
    """
    # Squelette : à implémenter plus tard
    raise NotImplementedError


def ev_for_match(
    model_probs: Dict[str, float],
    odds: Dict[str, float],
) -> Dict[str, float]:
    """
    Calcule l'EV pour chaque issue (1, X, 2) d'un match.

    Args:
        model_probs: Dict {"1": p1, "X": pX, "2": p2} (probas modèle).
        odds: Dict {"1": odd1, "X": oddX, "2": odd2} (cotes bookmaker).

    Returns:
        Dict {"1": ev1, "X": evX, "2": ev2}.
    """
    # Squelette : à implémenter plus tard
    raise NotImplementedError
