# examples/backtest_football_example.py
"""
Exemple de backtest sur matchs de football.

Utilise :
- Un modèle de type Poisson / Dixon-Coles (simulé ici).
- Calibration des probabilités.
- Backtest avec cotes.
"""

import numpy as np
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.calibration import CalibrationManager
from app.backtest import BacktestEngine
from app.metrics import log_loss, brier_score


def simulate_football_matches(
    n_matches: int = 500,
    seed: int = 42,
):
    """
    Simule des matchs de football avec probas et cotes.

    Returns:
        probs_home: Probas victoire domicile (modèle).
        odds_home: Cotes domicile.
        y_home: 1 si domicile gagne, 0 sinon.
    """
    np.random.seed(seed)

    # Probas “réelles” simulées (un peu de variance)
    p_true_home = np.random.beta(2, 3, size=n_matches)

    # Probas “modèle” (avec bruit)
    noise = np.random.randn(n_matches) * 0.05
    probs_home = np.clip(p_true_home + noise, 0.05, 0.95)

    # Cotes décimales (avec marge bookmaker ~5%)
    margin = 1.05
    odds_home = 1 / (probs_home + 1e-6) * margin
    odds_home = np.clip(odds_home, 1.1, 10.0)

    # Résultats réels
    y_home = (np.random.rand(n_matches) < p_true_home).astype(int)

    return probs_home, odds_home, y_home


def main():
    print("=== Backtest football (exemple) ===
")

    # 1. Simuler des matchs
    probs_model, odds_home, y_true = simulate_football_matches(n_matches=500)

    # 2. Calibration
    manager = CalibrationManager(
        method="platt",
        recalibrate=False,
        drift_detection=False,
    )
    manager.fit(probs_model, y_true)
    probs_calib = manager.predict(probs_model)

    # 3. Métriques de calibration
    print("Calibration :")
    print(f"  Log Loss (avant) : {log_loss(y_true, probs_model):.4f}")
    print(f"  Log Loss (après) : {log_loss(y_true, probs_calib):.4f}")
    print(f"  Brier (avant)    : {brier_score(y_true, probs_model):.4f}")
    print(f"  Brier (après)    : {brier_score(y_true, probs_calib):.4f}")

    # 4. Backtest
    engine = BacktestEngine(
        initial_bankroll=1000.0,
        bet_size=10.0,
        bet_fraction=None,  # mise fixe
    )

    # Stratégie : parier domicile si proba calibrée > 0.6
    result = engine.run(
        probs=probs_calib,
        odds=odds_home,
        y_true=y_true,
        threshold_high=0.6,
        threshold_low=0.4,
    )

    print("
Résultats du backtest :")
    print(f"  PnL total        : {result.pnl:.2f}")
    print(f"  Sharpe           : {result.sharpe:.3f}")
    print(f"  Max Drawdown     : {result.max_drawdown:.2f}")
    print(f"  Nombre de paris  : {result.n_trades}")

    # Courbe de capital (derniers points)
    print("
Derniers points de l'equity curve :")
    print(result.equity_curve[-10:])


if __name__ == "__main__":
    main()
