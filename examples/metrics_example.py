# examples/metrics_example.py
"""
Exemple d'utilisation des métriques dans QFTE.

Montre :
- Comment calculer Log Loss, Brier score, ECE.
- Comment comparer plusieurs modèles.
"""

import numpy as np
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.metrics import log_loss, brier_score, expected_calibration_error


def main():
    np.random.seed(42)
    n_samples = 1000

    # Labels réels
    y_true = np.random.binomial(1, 0.3, size=n_samples)

    # Prédictions de 3 modèles simulés
    p_model_1 = np.random.rand(n_samples)  # Aléatoire
    p_model_2 = 0.3 + 0.4 * np.random.rand(n_samples)  # Mieux calibré
    p_model_3 = np.clip(
        y_true + 0.1 * np.random.randn(n_samples), 0, 1
    )  # Proche des labels

    models = {
        "Modèle 1 (aléatoire)": p_model_1,
        "Modèle 2 (mieux calibré)": p_model_2,
        "Modèle 3 (proche des labels)": p_model_3,
    }

    print("=== Comparaison de modèles ===
")
    print(f"{'Modèle':<30} | {'Log Loss':>10} | {'Brier':>8} | {'ECE':>8}")
    print("-" * 65)

    for name, p_pred in models.items():
        ll = log_loss(y_true, p_pred)
        bs = brier_score(y_true, p_pred)
        ece = expected_calibration_error(y_true, p_pred)
        print(f"{name:<30} | {ll:>10.4f} | {bs:>8.4f} | {ece:>8.4f}")


if __name__ == "__main__":
    main()
