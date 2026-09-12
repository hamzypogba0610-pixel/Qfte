# examples/experiment_example.py
"""
Exemple d'utilisation de app.experiments.

Montre :
- Définition d'une config.
- Lancement d'une expérience.
- Affichage des métriques.
"""

import numpy as np
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.experiments import ExperimentConfig, run_experiment
from app.data import train_test_split


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

    return X, y


def main():
    print("=== Exemple d'expérience QFTE ===
")

    # 1. Données
    X, y = generate_data(n_samples=2000)

    # 2. Config
    config = ExperimentConfig(
        model_name="logistic",
        model_kwargs={"lr": 0.1, "n_epochs": 100},
        calibration_method="platt",
        recalibrate=True,
        recalibration_period=500,
        drift_detection=True,
        test_size=0.3,
        random_state=42,
        normalize=True,
        metrics=["log_loss", "brier", "ece"],
    )

    # 3. Lancement
    metrics = run_experiment(X, y, config)

    # 4. Affichage
    print("Métriques sur le test set :")
    for name, value in metrics.items():
        print(f"  {name}: {value:.4f}")

    # 5. Comparaison sans calibration
    print("
=== Sans calibration ===
")

    config_no_calib = ExperimentConfig(
        model_name="logistic",
        model_kwargs={"lr": 0.1, "n_epochs": 100},
        calibration_method="none",
        recalibrate=False,
        test_size=0.3,
        random_state=42,
        normalize=True,
        metrics=["log_loss", "brier", "ece"],
    )

    metrics_no_calib = run_experiment(X, y, config_no_calib)

    print("Métriques sans calibration :")
    for name, value in metrics_no_calib.items():
        print(f"  {name}: {value:.4f}")


if __name__ == "__main__":
    main()
