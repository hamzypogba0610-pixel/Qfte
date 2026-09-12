# app/backtest/engine.py
"""
Moteur de backtest simple pour QFTE.
"""

from __future__ import annotations

import numpy as np
from typing import Optional, Tuple
from dataclasses import dataclass


@dataclass
class BacktestResult:
    """Résultat d'un backtest."""
    pnl: float
    sharpe: float
    max_drawdown: float
    hit_rate: float
    n_trades: int
    equity_curve: np.ndarray


class BacktestEngine:
    """
    Moteur de backtest simple.

    Stratégie :
    - Si proba > seuil_haut → pari "over" ou équipe A.
    - Si proba < seuil_bas → pari "under" ou équipe B.
    - Mise fixe ou fraction de bankroll.
    """

    def __init__(
        self,
        initial_bankroll: float = 1000.0,
        bet_size: float = 10.0,
        bet_fraction: Optional[float] = None,
    ):
        self.initial_bankroll = initial_bankroll
        self.bet_size = bet_size
        self.bet_fraction = bet_fraction  # si != None, mise = fraction * bankroll

    def _get_bet_size(self, bankroll: float) -> float:
        if self.bet_fraction is not None:
            return bankroll * self.bet_fraction
        return self.bet_size

    def run(
        self,
        probs: np.ndarray,
        odds: np.ndarray,
        y_true: np.ndarray,
        threshold_high: float = 0.6,
        threshold_low: float = 0.4,
    ) -> BacktestResult:
        """
        Lance le backtest.

        Args:
            probs: Probabilités prédites (pour l'outcome parié).
            odds: Cotes décimales pour cet outcome.
            y_true: Résultats réels (1 si gagné, 0 si perdu).
            threshold_high: Seuil haut pour parier.
            threshold_low: Seuil bas pour parier l'inverse.

        Returns:
            BacktestResult.
        """
        n = len(probs)
        equity = np.zeros(n + 1)
        equity = self.initial_bankroll
        bankroll = self.initial_bankroll

        n_trades = 0

        for i in range(n):
            p = probs[i]
            odd = odds[i]
            y = y_true[i]

            # Décision de pari
            bet = 0.0  # 0 = pas de pari, 1 = pari sur l'outcome
            if p > threshold_high:
                bet = 1.0
            elif p < threshold_low:
                # On pourrait parier l'inverse, ici on skip pour simplifier
                bet = 0.0

            if bet == 0.0:
                equity[i + 1] = equity[i]
                continue

            # Taille du pari
            stake = self._get_bet_size(bankroll)
            n_trades += 1

            # PnL du pari
            if y == 1:
                pnl = stake * (odd - 1)
            else:
                pnl = -stake

            bankroll += pnl
            equity[i + 1] = bankroll

        equity_curve = equity

        # Métriques
        from .metrics import (
            calculate_pnl,
            calculate_sharpe,
            calculate_max_drawdown,
            calculate_hit_rate,
        )

        pnl = calculate_pnl(equity_curve)
        sharpe = calculate_sharpe(equity_curve)
        max_dd = calculate_max_drawdown(equity_curve)

        # Hit rate (simplifié : proportion de paris gagnants)
        # On va le recalculer proprement dans un vrai backtest
        hit_rate = 0.0  # à améliorer si on stocke les paris individuels

        return BacktestResult(
            pnl=pnl,
            sharpe=sharpe,
            max_drawdown=max_dd,
            hit_rate=hit_rate,
            n_trades=n_trades,
            equity_curve=equity_curve,
        )
