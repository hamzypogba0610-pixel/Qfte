# QFTE

QFTE est un projet Python pour l’entraînement et l’évaluation de modèles de prédiction, avec un accent sur la calibration des probabilités.

## Structure principale

- `app/calibration/` : méthodes de calibration (Platt, Isotonic, Beta, Temperature Scaling, etc.) et recalibration adaptative.
- `app/models/` : modèles de classification :
  - `LogisticRegression`
  - `GaussianNaiveBayes`
  - `SimpleDecisionTree`
  - ainsi que des modèles de scores (Poisson, Dixon-Coles, etc.).
- `app/metrics/` : métriques (Log Loss, Brier score, ECE, etc.).
- `app/data/` : chargement et préprocessing des données.
- `app/utils/` : utilitaires (I/O, validation, etc.).
- `app/experiments/` : configurations et lancement d’expériences.
- `app/backtest/` : moteur de backtest et métriques de performance (PnL, Sharpe, drawdown, etc.).
- `examples/` : scripts d’exemple pour chaque module.

  ## Exemples

Voir le dossier `examples/` :

```bash
# Démarrage rapide
python examples/quickstart.py

# Calibration seule
python examples/calibration_example.py

# Modèle + calibration
python examples/logistic_calibration_example.py

# Pipeline complet avec data
python examples/full_data_pipeline_example.py

# Expériences configurées
python examples/experiment_example.py

# Comparaison de modèles
python examples/compare_models_example.py

```bash
# Backtest football
python examples/backtest_football_example.py
***

## Partie 4 – Installation

## Installation
...

## Licence
...
