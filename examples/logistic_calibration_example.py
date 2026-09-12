# examples/logistic_calibration_example.py
"""
Exemple : LogisticRegression + calibration.

Montre :
- Entraînement d'une régression logistique.
- Calibration des probabilités.
- Comparaison avant/après calibration.
"""

import numpy as np
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.models import LogisticRegression
from app.calibration import CalibrationManager
from app.metrics import log_loss, brier_score, expected_calibration_error


def generate_data(
    n_samples: int = 2000,
    noise: float = 0.1,
    seed: int = 42,
):
    """Génère des données synthétiques pour classification binaire."""
    np.random.seed(seed)

    X = np.random.randn(n_samples, 5)
    true_coef = np.array([1.5, -2.0, 0.5, 1.0, -1.5])
    logits = X @ true_coef + noise * np.random.randn(n_samples)

    p_true = 1 / (1 + np.exp(-logits))
    y = np.random.binomial(1, p_true)

    return X, y, p_true


def main():
    print("=== LogisticRegression + calibration ===
")

    # 1. Données
    X, y, _ = generate_data(n_samples=2000)

    split = int(0.7 * len(y))
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    # 2. Modèle
    model = LogisticRegression(lr=0.1, n_epochs=100, fit_intercept=True)
    model.fit(X_train, y_train)

    # 3. Prédictions brutes
    p_raw = model.predict_proba(X_test)

    # 4. Calibration
    manager = CalibrationManager(
        method="platt",
        recalibrate=True,
        recalibration_period=500,
        drift_detection=True,
        buffer_size=2000,
    )

    manager.fit(p_raw, y_test)
    p_calibrated = manager.predict(p_raw)

    # 5. Évaluation
    print("Avant calibration :")
    print(f"  Log Loss : {log_loss(y_test, p_raw):.4f}")
    print(f"  Brier    : {brier_score(y_test, p_raw):.4f}")
    print(f"  ECE      : {expected_calibration_error(y_test, p_raw):.4f}")

    print("
Après calibration :")
    print(f"  Log Loss : {log_loss(y_test, p_calibrated):.4f}")
    print(f"  Brier    : {brier_score(y_test, p_calibrated):.4f}")
    print(f"  ECE      : {expected_calibration_error(y_test, p_calibrated):.4f}")

    # 6. Prédiction sur nouveaux points
    X_new = np.random.randn(5, 5)
    p_raw_new = model.predict_proba(X_new)
    p_calib_new = manager.predict(p_raw_new)

    print("
Nouvelles prédictions calibrées :")
    for raw, calib in zip(p_raw_new, p_calib_new):
        print(f"  {raw:.3f} → {calib:.3f}")


if __name__ == "__main__":
    main()
