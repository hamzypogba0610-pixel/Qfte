# app/api/bankroll.py
"""
Gestion de la bankroll pour QFTE.

Ce module fournira :
- Le suivi de la bankroll (solde, historique des mises, P&L).
- La logique pour la future commande Telegram /risk.
- Des utilitaires pour calculer la mise recommandée par pari.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional

from ..engines.risk import BankrollConfig, compute_stake, kelly_fraction_adjusted


@dataclass
class BetRecord:
    """
    Enregistrement d'un pari placé.
    """
    match_id: int
    outcome: str              # "1", "X" ou "2"
    stake: float              # Mise en unités monétaires
    odd: float                # Cote décimale
    result: Optional[str] = None  # "W" (win), "L" (loss), "V" (void), None si en cours
    pnl: Optional[float] = None   # Profit & Loss (stake * odd - stake si win, -stake si loss)
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class BankrollState:
    """
    État actuel de la bankroll.
    """
    initial_bankroll: float
    current_bankroll: float
    total_staked: float = 0.0
    total_pnl: float = 0.0
    bets: List[BetRecord] = field(default_factory=list)
    config: Optional[BankrollConfig] = None


def update_bankroll_after_bet(
    state: BankrollState,
    bet: BetRecord,
) -> BankrollState:
    """
    Met à jour la bankroll après un pari (avant résultat).

    Args:
        state: État actuel de la bankroll.
        bet: Pari placé.

    Returns:
        Nouvel état de la bankroll.
    """
    # Squelette : à implémenter plus tard
    raise NotImplementedError


def settle_bet(
    state: BankrollState,
    bet_index: int,
    result: str,  # "W", "L" ou "V"
) -> BankrollState:
    """
    Règle un pari (win/loss/void) et met à jour la bankroll.

    Args:
        state: État actuel de la bankroll.
        bet_index: Index du pari dans state.bets.
        result: "W" (win), "L" (loss), "V" (void).

    Returns:
        Nouvel état de la bankroll.
    """
    # Squelette : à implémenter plus tard
    raise NotImplementedError


def recommended_stake_for_bet(
    win_prob: float,
    decimal_odd: float,
    config: BankrollConfig,
) -> float:
    """
    Calcule la mise recommandée pour un pari (wrapper autour de compute_stake).

    Args:
        win_prob: Probabilité de gain (0..1).
        decimal_odd: Cote décimale.
        config: BankrollConfig.

    Returns:
        Mise recommandée (0 si pas de pari).
    """
    # Squelette : à implémenter plus tard
    raise NotImplementedError
