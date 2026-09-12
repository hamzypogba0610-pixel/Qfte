# examples/calibration_example.py
"""
Exemple d'utilisation de la calibration dans QFTE.

Montre :
- Comment calibrer des probabilités brutes.
- Comment activer la recalibration adaptative.
- Comment évaluer la calibration (Log Loss, Brier score, ECE).
"""

import numpy as np
from pathlib import Path

# Pour importer depuis le projet
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.calibration import CalibrationManager
from app.metrics import log_loss, brier_score, expected_calibration_error


def main():
    # Données simulées
    np.random.seed(42)
    n_samples = 2000

    # Probabilités brutes (sortie d'un modèle)
    p_raw = np.random.beta(2, 5, size=n_samples)  # Déséquilibré vers 0

    # Labels réels (avec un peu de bruit)
    y = (np.random.rand(n_samples) < p_raw).astype(int)

    # Split train / test
    split = int(0.7 * n_samples)
    p_train, p_test = p_raw[:split], p_raw[split:]
    y_train, y_test = y[:split], y[split:]

    # --- Calibration avec recalibration activée ---
    manager = CalibrationManager(
        method="platt",
        recalibrate=True,
        recalibration_period=500,
        drift_detection=True,
        buffer_size=2000,
    )

    # Entraînement
    manager.fit(p_train, y_train)

    # Prédiction calibrée
    p_calibrated = manager.predict(p_test)

    # --- Métriques avant/après calibration ---
    print("=== Calibration avec recalibration adaptative ===
")

    print("Avant calibration (p_raw) :")
    print(f"  Log Loss : {log_loss(y_test, p_test):.4f}")
    print(f"  Brier    : {brier_score(y_test, p_test):.4f}")
    print(f"  ECE      : {expected_calibration_error(y_test, p_test):.4f}")

    print("
Après calibration (p_calibrated) :")
    print(f"  Log Loss : {log_loss(y_test, p_calibrated):.4f}")
    print(f"  Brier    : {brier_score(y_test, p_calibrated):.4f}")
    print(f"  ECE      : {expected_calibration_error(y_test, p_calibrated):.4f}")

    # --- Mise à jour en ligne (simulation) ---
    print("
=== Mise à jour en ligne (100 nouvelles observations) ===
")

    n_online = 100
    p_online = np.random.beta(2, 5, size=n_online)
    y_online = (np.random.rand(n_online) < p_online).astype(int)

    n_recalib = 0
    for p, label in zip(p_online, y_online):
        if manager.update(float(p), int(label)):
            n_recalib += 1

    print(f"Nombre de recalibrations déclenchées : {n_recalib}")

    # Prédiction sur un nouvel échantillon
    p_new = np.array([0.3, 0.5, 0.7])
    p_new_calib = manager.predict(p_new)

    print("
Nouvelles prédictions calibrées :")
    for raw, calib in zip(p_new, p_new_calib):
        print(f"  {raw:.3f} → {calib:.3f}")


if __name__ == "__main__":
    main()
