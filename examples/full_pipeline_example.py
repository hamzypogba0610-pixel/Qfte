# examples/full_pipeline_example.py
"""
Exemple de pipeline complet pour QFTE.

Montre :
- Génération de données synthétiques.
- Entraînement d'un modèle simple.
- Calibration des probabilités.
- Évaluation avec métriques.
- Mise à jour en ligne avec recalibration.
"""

import numpy as np
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.calibration import CalibrationManager
from app.metrics import log_loss, brier_score, expected_calibration_error


def generate_data(
    n_samples: int = 2000,
    noise: float = 0.1,
    seed: int = 42,
):
    """Génère des données synthétiques pour classification binaire."""
    np.random.seed(seed)

    # Features
    X = np.random.randn(n_samples, 5)

    # Vrais coefficients
    true_coef = np.array([1.5, -2.0, 0.5, 1.0, -1.5])
    logits = X @ true_coef + noise * np.random.randn(n_samples)

    # Probabilités vraies
    p_true = 1 / (1 + np.exp(-logits))

    # Labels
    y = np.random.binomial(1, p_true)

    return X, y, p_true


def train_simple_model(X_train, y_train):
    """
    Modèle très simple : régression logistique 'maison'.
    Retourne les poids et une fonction de prédiction.
    """
    # Initialisation
    n_features = X_train.shape[1]
    weights = np.zeros(n_features)
    bias = 0.0

    lr = 0.1
    n_epochs = 100

    for _ in range(n_epochs):
        logits = X_train @ weights + bias
        p_pred = 1 / (1 + np.exp(-logits))

        # Gradient
        error = p_pred - y_train
        grad_w = (X_train.T @ error) / len(y_train)
        grad_b = np.mean(error)

        # Mise à jour
        weights -= lr * grad_w
        bias -= lr * grad_b

    def predict_proba(X):
        logits = X @ weights + bias
        return 1 / (1 + np.exp(-logits))

    return predict_proba


def main():
    print("=== Pipeline complet QFTE ===
")

    # 1. Génération des données
    X, y, p_true = generate_data(n_samples=2000)

    # Split train / test
    split = int(0.7 * len(y))
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]
    p_true_test = p_true[split:]

    # 2. Entraînement du modèle
    predict_proba = train_simple_model(X_train, y_train)

    # 3. Prédictions brutes
    p_raw_test = predict_proba(X_test)

    # 4. Calibration
    manager = CalibrationManager(
        method="platt",
        recalibrate=True,
        recalibration_period=500,
        drift_detection=True,
        buffer_size=2000,
    )

    manager.fit(p_raw_test, y_test)
    p_calibrated = manager.predict(p_raw_test)

    # 5. Évaluation
    print("Avant calibration :")
    print(f"  Log Loss : {log_loss(y_test, p_raw_test):.4f}")
    print(f"  Brier    : {brier_score(y_test, p_raw_test):.4f}")
    print(f"  ECE      : {expected_calibration_error(y_test, p_raw_test):.4f}")

    print("
Après calibration :")
    print(f"  Log Loss : {log_loss(y_test, p_calibrated):.4f}")
    print(f"  Brier    : {brier_score(y_test, p_calibrated):.4f}")
    print(f"  ECE      : {expected_calibration_error(y_test, p_calibrated):.4f}")

    # 6. Mise à jour en ligne (simulation de drift)
    print("
=== Mise à jour en ligne (simulation de drift) ===
")

    n_online = 300
    X_online, y_online, _ = generate_data(
        n_samples=n_online,
        noise=0.2,
        seed=123,
    )

    p_raw_online = predict_proba(X_online)

    n_recalib = 0
    for p_raw, y_true in zip(p_raw_online, y_online):
        if manager.update(float(p_raw), int(y_true)):
            n_recalib += 1

    print(f"Nombre de recalibrations déclenchées : {n_recalib}")

    # Prédiction sur quelques nouveaux points
    X_new = np.random.randn(5, 5)
    p_raw_new = predict_proba(X_new)
    p_calib_new = manager.predict(p_raw_new)

    print("
Nouvelles prédictions calibrées :")
    for raw, calib in zip(p_raw_new, p_calib_new):
        print(f"  {raw:.3f} → {calib:.3f}")


if __name__ == "__main__":
    main()
