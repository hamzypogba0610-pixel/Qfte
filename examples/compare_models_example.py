# examples/compare_models_example.py
"""
Comparaison de modèles avec et sans calibration.

Modèles :
- LogisticRegression
- GaussianNaiveBayes
- SimpleDecisionTree

Métriques :
- Log Loss
- Brier score
- ECE
"""

import numpy as np
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.models import (
    LogisticRegression,
    GaussianNaiveBayes,
    SimpleDecisionTree,
)
from app.calibration import CalibrationManager
from app.data import train_test_split, StandardScaler
from app.metrics import log_loss, brier_score, expected_calibration_error


def generate_data(
    n_samples: int = 2000,
    noise: float = 0.1,
    seed: int = 42,
):
    """Génère des données synthétiques."""
    np.random.seed(seed)

    X = np.random.randn(n_samples, 5)
    true_coef = np.array([1.5, -2.0, 0.5, 1.0, -1.5])
    logits = X @ true_coef + noise * np.random.randn(n_samples)

    p_true = 1 / (1 + np.exp(-logits))
    y = np.random.binomial(1, p_true)

    return X, y


def evaluate_model(
    model,
    X_train,
    X_test,
    y_train,
    y_test,
    calibrate: bool = False,
):
    """Évalue un modèle avec ou sans calibration."""
    model.fit(X_train, y_train)
    p_raw = model.predict_proba(X_test)

    if calibrate:
        manager = CalibrationManager(
            method="platt",
            recalibrate=False,
            drift_detection=False,
        )
        manager.fit(p_raw, y_train)
        p_pred = manager.predict(p_raw)
    else:
        p_pred = p_raw

    return {
        "log_loss": log_loss(y_test, p_pred),
        "brier": brier_score(y_test, p_pred),
        "ece": expected_calibration_error(y_test, p_pred),
    }


def main():
    print("=== Comparaison de modèles ===
")

    # 1. Données
    X, y = generate_data(n_samples=2000)

    # 2. Split + normalisation
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # 3. Modèles
    models = {
        "LogisticRegression": LogisticRegression(lr=0.1, n_epochs=100),
        "GaussianNaiveBayes": GaussianNaiveBayes(),
        "SimpleDecisionTree": SimpleDecisionTree(max_depth=2, min_samples_leaf=10),
    }

    # 4. Résultats
    results = []

    for name, model in models.items():
        for calib in [False, True]:
            metrics = evaluate_model(
                model,
                X_train,
                X_test,
                y_train,
                y_test,
                calibrate=calib,
            )

            results.append(
                {
                    "Modèle": name,
                    "Calibration": "Oui" if calib else "Non",
                    **metrics,
                }
            )

    # 5. Affichage
    header = f"{'Modèle':<25} | {'Calib':<8} | {'Log Loss':>10} | {'Brier':>8} | {'ECE':>8}"
    print(header)
    print("-" * len(header))

    for r in results:
        print(
            f"{r['Modèle']:<25} | {r['Calibration']:<8} | "
            f"{r['log_loss']:>10.4f} | {r['brier']:>8.4f} | {r['ece']:>8.4f}"
        )


if __name__ == "__main__":
    main()
