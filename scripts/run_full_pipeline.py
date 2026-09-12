# scripts/run_full_pipeline.py
"""
Pipeline complet : data → calibration → backtest.

Utilisation :
    python scripts/run_full_pipeline.py
"""

import numpy as np
from pathlib import Path
import csv

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.calibration import CalibrationManager
from app.backtest import BacktestEngine
from app.metrics import log_loss, brier_score, expected_calibration_error


def load_matches(csv_path: str):
    """
    Charge les matchs depuis un CSV.

    Returns:
        probs_home, odds_home, y_home
    """
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    probs = []
    odds = []
    y = []

    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            probs.append(float(row["proba_home"]))
            odds.append(float(row["odd_home"]))
            y.append(int(row["y_home"]))

    return np.array(probs), np.array(odds), np.array(y)


def main():
    print("=== QFTE – Pipeline complet ===
")

    # 1. Charger les données
    csv_path = Path(__file__).parent.parent / "data" / "sample_matches.csv"
    probs_model, odds_home, y_true = load_matches(str(csv_path))

    print(f"Nombre de matchs : {len(y_true)}
")

    # 2. Calibration
    manager = CalibrationManager(
        method="platt",
        recalibrate=False,
        drift_detection=False,
    )
    manager.fit(probs_model, y_true)
    probs_calib = manager.predict(probs_model)

    print("Calibration :")
    print(f"  Log Loss (avant) : {log_loss(y_true, probs_model):.4f}")
    print(f"  Log Loss (après) : {log_loss(y_true, probs_calib):.4f}")
    print(f"  Brier (avant)    : {brier_score(y_true, probs_model):.4f}")
    print(f"  Brier (après)    : {brier_score(y_true, probs_calib):.4f}")
    print(f"  ECE (avant)      : {expected_calibration_error(y_true, probs_model):.4f}")
    print(f"  ECE (après)      : {expected_calibration_error(y_true, probs_calib):.4f}")

    # 3. Backtest
    engine = BacktestEngine(
        initial_bankroll=1000.0,
        bet_size=10.0,
        bet_fraction=None,
    )

    result = engine.run(
        probs=probs_calib,
        odds=odds_home,
        y_true=y_true,
        threshold_high=0.6,
        threshold_low=0.4,
    )

    print("
Backtest :")
    print(f"  PnL total        : {result.pnl:.2f}")
    print(f"  Sharpe           : {result.sharpe:.3f}")
    print(f"  Max Drawdown     : {result.max_drawdown:.2f}")
    print(f"  Nombre de paris  : {result.n_trades}")

    print("
Equity curve (début → fin) :")
    print(f"  Start : {result.equity_curve:.2f}")
    print(f"  End   : {result.equity_curve[-1]:.2f}")


if __name__ == "__main__":
    main()
