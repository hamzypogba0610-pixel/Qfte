# examples/full_data_pipeline_example.py
"""
Pipeline complet avec data + models + calibration.

Montre :
- Génération d'un CSV simulé.
- Chargement avec app.data.
- Préprocessing (split + normalisation).
- Modèle + calibration.
- Évaluation.
"""

import numpy as np
from pathlib import Path
import csv
import tempfile

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.data import load_csv, train_test_split, StandardScaler
from app.models import LogisticRegression
from app.calibration import CalibrationManager
from app.metrics import log_loss, brier_score, expected_calibration_error


def generate_csv(
    n_samples: int = 1000,
    seed: int = 42,
) -> str:
    """Génère un CSV temporaire avec des données synthétiques."""
    np.random.seed(seed)

    # Features
    X = np.random.randn(n_samples, 4)
    col_names = [f"feat_{i}" for i in range(4)]

    # Target binaire
    true_coef = np.array([1.0, -1.5, 0.5, 1.0])
    logits = X @ true_coef + 0.2 * np.random.randn(n_samples)
    p_true = 1 / (1 + np.exp(-logits))
    y = np.random.binomial(1, p_true)

    # Écriture CSV
    tmp = tempfile.NamedTemporaryFile(
        mode="w", delete=False, suffix=".csv", newline=""
    )
    writer = csv.writer(tmp)

    writer.writerow(col_names + ["target"])
    for i in range(n_samples):
        writer.writerow(list(X[i]) + [int(y[i])])

    tmp.close()
    return tmp.name


def main():
    print("=== Pipeline complet : data + models + calibration ===
")

    # 1. Générer un CSV simulé
    csv_path = generate_csv(n_samples=1000)

    try:
        # 2. Chargement
        X, y = load_csv(
            csv_path,
            target_column="target",
            feature_columns=None,  # utilise toutes les autres colonnes
        )

        # 3. Split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=42
        )

        # 4. Normalisation
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # 5. Modèle
        model = LogisticRegression(lr=0.1, n_epochs=100, fit_intercept=True)
        model.fit(X_train_scaled, y_train)

        # 6. Prédictions brutes
        p_raw = model.predict_proba(X_test_scaled)

        # 7. Calibration
        manager = CalibrationManager(
            method="platt",
            recalibrate=True,
            recalibration_period=300,
            drift_detection=True,
            buffer_size=1000,
        )

        manager.fit(p_raw, y_test)
        p_calibrated = manager.predict(p_raw)

        # 8. Évaluation
        print("Avant calibration :")
        print(f"  Log Loss : {log_loss(y_test, p_raw):.4f}")
        print(f"  Brier    : {brier_score(y_test, p_raw):.4f}")
        print(f"  ECE      : {expected_calibration_error(y_test, p_raw):.4f}")

        print("
Après calibration :")
        print(f"  Log Loss : {log_loss(y_test, p_calibrated):.4f}")
        print(f"  Brier    : {brier_score(y_test, p_calibrated):.4f}")
        print(f"  ECE      : {expected_calibration_error(y_test, p_calibrated):.4f}")

    finally:
        # Nettoyage du fichier temporaire
        Path(csv_path).unlink(missing_ok=True)


if __name__ == "__main__":
    main()
