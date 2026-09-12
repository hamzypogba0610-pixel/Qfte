# app/engines/__init__.py
"""
Moteurs de décision et de marché pour QFTE.

- market: calcul des cotes implicites, EV, etc.
- decision: règles BET / WATCH / PASS.
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

__all__ = [
    "implied_probs_from_odds",
    "ev_for_outcome",
    "ev_for_match",
    "Decision",
    "DecisionContext",
    "decide_bet",
    "build_decision_context",
]
