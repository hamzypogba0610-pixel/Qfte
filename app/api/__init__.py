# app/api/__init__.py
"""
API et logique métier pour QFTE.

- scanner: scan des matchs, EV, décision, top bets.
- bankroll: gestion de la bankroll, historique des paris, /risk.
"""

from .scanner import (
    ScanResult,
    scan_match,
    top_bets,
)

from .bankroll import (
    BetRecord,
    BankrollState,
    update_bankroll_after_bet,
    settle_bet,
    recommended_stake_for_bet,
)

__all__ = [
    "ScanResult",
    "scan_match",
    "top_bets",
    "BetRecord",
    "BankrollState",
    "update_bankroll_after_bet",
    "settle_bet",
    "recommended_stake_for_bet",
]
