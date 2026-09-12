# app/models/backtest.py
"""
Backtest walk-forward pour les modèles de prédiction de scores.

Ce module fournit :
- Une fonction pour diviser les données en fenêtres d'entraînement/test.
- Une boucle de backtest qui entraîne et évalue le modèle sur chaque fenêtre.
"""

from __future__ import annotations

from typing import Callable, Dict, List, Any


def walk_forward_splits(
    matches: List[Dict],
    train_seasons: int = 3,
    test_seasons: int = 1,
) -> List[Dict[str, List[Dict]]]:
    """
    Divise les données en fenêtres d'entraînement/test (walk-forward).

    Args:
        matches: Liste de matchs triés par saison/date.
        train_seasons: Nombre de saisons pour l'entraînement.
        test_seasons: Nombre de saisons pour le test.

    Returns:
        Liste de dicts {"train": [...], "test": [...]}.
    """
    # Squelette : à implémenter plus tard
    raise NotImplementedError


def run_backtest(
    matches: List[Dict],
    model_factory: Callable,
    metrics_fns: List[Callable],
    train_seasons: int = 3,
    test_seasons: int = 1,
) -> Dict[str, Any]:
    """
    Exécute un backtest walk-forward.

    Args:
        matches: Liste de matchs triés par saison/date.
        model_factory: Fonction qui crée un modèle (ex: fit_dixon_coles).
        metrics_fns: Liste de fonctions de métriques (Brier, Log Loss, etc.).
        train_seasons: Nombre de saisons pour l'entraînement.
        test_seasons: Nombre de saisons pour le test.

    Returns:
        Dict avec les résultats du backtest (métriques par fenêtre, moyennes, etc.).
    """
    # Squelette : à implémenter plus tard
    raise NotImplementedError
