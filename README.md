# QFTE

QFTE est un projet Python pour l’entraînement et l’évaluation de modèles de prédiction, avec un accent sur la calibration des probabilités.

## Structure principale

- `app/calibration/` : méthodes de calibration (Platt, Isotonic, Beta, etc.) et recalibration adaptative.
- `app/models/` : modèles de classification (logistic regression, etc.) et modèles de scores.
- `app/metrics/` : métriques (Log Loss, Brier score, ECE, etc.).
- `app/data/` : chargement et préprocessing des données.
- `app/utils/` : utilitaires (I/O, validation, etc.).
- `examples/` : scripts d’exemple pour chaque module.

## Exemples

Voir le dossier `examples/` :

```bash
python examples/calibration_example.py
python examples/logistic_calibration_example.py
python examples/full_data_pipeline_example.py
git clone <ton-depot>
cd Qfte
