# app/backtest/__init__.py
"""
Module backtest pour QFTE.

Fournit :
- Moteur de backtest simple.
- Métriques de performance (PnL, Sharpe, drawdown, etc.).
"""

from .engine import BacktestEngine
from .metrics import (
    calculate_pnl,
    calculate_sharpe,
    calculate_max_drawdown,
    calculate_hit_rate,
)

__all__: list[str] = [
    "BacktestEngine",
    "calculate_pnl",
    "calculate_sharpe",
    "calculate_max_drawdown",
    "calculate_hit_rate",
]
