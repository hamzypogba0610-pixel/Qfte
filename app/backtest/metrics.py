# app/backtest/metrics.py
"""
Métriques de performance pour backtest.
"""

from __future__ import annotations

import numpy as np


def calculate_pnl(equity_curve: np.ndarray) -> float:
    """
    PnL total (final - initial).

    Args:
        equity_curve: Courbe de capital (inclut le point initial).

    Returns:
        PnL total.
    """
    return float(equity_curve[-1] - equity_curve)


def calculate_sharpe(
    equity_curve: np.ndarray,
    risk_free_rate: float = 0.0,
    periods_per_year: int = 252,
) -> float:
    """
    Ratio de Sharpe annualisé.

    Args:
        equity_curve: Courbe de capital.
        risk_free_rate: Taux sans risque (annualisé).
        periods_per_year: Nombre de périodes par an.

    Returns:
        Sharpe annualisé.
    """
    returns = np.diff(equity_curve) / equity_curve[:-1]

    if len(returns) < 2:
        return 0.0

    excess_returns = returns - risk_free_rate / periods_per_year
    mean_ret = np.mean(excess_returns)
    std_ret = np.std(excess_returns, ddof=1)

    if std_ret == 0:
        return 0.0

    sharpe = mean_ret / std_ret
    sharpe_annualized = sharpe * np.sqrt(periods_per_year)

    return float(sharpe_annualized)


def calculate_max_drawdown(equity_curve: np.ndarray) -> float:
    """
    Drawdown maximum (en valeur absolue).

    Args:
        equity_curve: Courbe de capital.

    Returns:
        Max drawdown (négatif ou 0).
    """
    peak = np.maximum.accumulate(equity_curve)
    drawdown = equity_curve - peak
    return float(np.min(drawdown))


def calculate_hit_rate(
    bets: np.ndarray,
    outcomes: np.ndarray,
) -> float:
    """
    Taux de réussite (hit rate).

    Args:
        bets: 1 si pari, 0 sinon.
        outcomes: 1 si pari gagné, 0 si perdu (pour les paris).

    Returns:
        Hit rate (0–1).
    """
    mask = bets == 1
    if np.sum(mask) == 0:
        return 0.0

    return float(np.mean(outcomes[mask]))
