# app/engines/__init__.py
"""
Moteurs de décision, de marché et de risque pour QFTE.

- market: calcul des cotes implicites, EV, etc.
- decision: règles BET / WATCH / PASS.
- risk: Kelly, bankroll, limites de mise, score de risque.
"""

from .market import (
    implied_probs_from_odds,
    ev_for_outcome,
    ev_for_match,
)

from .decision import (
    Decision,
    DecisionContext,
    decide_bet,
    build_decision_context,
)

from .risk import (
    BankrollConfig,
    kelly_fraction_full,
    kelly_fraction_adjusted,
    compute_stake,
    risk_score,
)

__all__ = [
    "implied_probs_from_odds",
    "ev_for_outcome",
    "ev_for_match",
    "Decision",
    "DecisionContext",
    "decide_bet",
    "build_decision_context",
    "BankrollConfig",
    "kelly_fraction_full",
    "kelly_fraction_adjusted",
    "compute_stake",
    "risk_score",
]
