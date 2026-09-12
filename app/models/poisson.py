# app/models/poisson.py
"""
Poisson bivarié pour la prédiction de scores de football.

Ce module fournit des fonctions pour :
- Estimer les paramètres lambda (intensités de buts) pour chaque équipe.
- Calculer la distribution conjointe des scores (home_goals, away_goals).
- Générer des probabilités 1X2, Over/Under, etc.
"""

from __future__ import annotations

import math
from typing import Dict, List, Tuple

import numpy as np
from scipy.stats import poisson


def estimate_lambdas(
    matches: List[Dict],
    team_ids: List[int],
) -> Dict[int, float]:
    """
    Estime les lambdas (intensités de buts) pour chaque équipe.

    Args:
        matches: Liste de matchs avec home_team_id, away_team_id, home_goals, away_goals.
        team_ids: Liste des identifiants d'équipes.

    Returns:
        Dict mapping team_id -> lambda (expected goals per match).
    """
    # Squelette : à implémenter plus tard
    raise NotImplementedError


def joint_score_distribution(
    lambda_home: float,
    lambda_away: float,
    max_goals: int = 6,
) -> np.ndarray:
    """
    Calcule la distribution conjointe P(home_goals, away_goals).

    Args:
        lambda_home: Intensité de buts de l'équipe à domicile.
        lambda_away: Intensité de buts de l'équipe à l'extérieur.
        max_goals: Nombre maximum de buts à considérer (0..max_goals).

    Returns:
        Matrice (max_goals+1, max_goals+1) de probabilités.
    """
    # Squelette : à implémenter plus tard
    raise NotImplementedError


def probs_1x2_from_joint(joint: np.ndarray) -> Dict[str, float]:
    """
    Calcule les probabilités 1X2 à partir de la distribution conjointe.

    Args:
        joint: Matrice de probabilités P(home_goals, away_goals).

    Returns:
        Dict {"1": p_home, "X": p_draw, "2": p_away}.
    """
    # Squelette : à implémenter plus tard
    raise NotImplementedError
