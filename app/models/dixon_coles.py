# app/models/dixon_coles.py
"""
Modèle de Dixon-Coles.

Améliore le modèle de Poisson en ajustant les probabilités
des petits scores (0-0, 1-0, 0-1, 1-1) via un paramètre rho.
"""

from __future__ import annotations

from typing import Dict, List, Tuple

import numpy as np


def fit_dixon_coles(
    matches: List[Dict],
    team_ids: List[int],
) -> Tuple[Dict[int, float], float]:
    """
    Ajuste un modèle Dixon-Coles sur des matchs historiques.

    Returns:
        - lambdas: Dict team_id -> lambda (intensité de buts).
        - rho: Paramètre de correction pour les petits scores.
    """
    # Squelette : à implémenter plus tard
    raise NotImplementedError


def joint_score_distribution_dc(
    lambda_home: float,
    lambda_away: float,
    rho: float,
    max_goals: int = 6,
) -> np.ndarray:
    """
    Calcule la distribution conjointe avec correction Dixon-Coles.

    Args:
        lambda_home: Intensité de buts de l'équipe à domicile.
        lambda_away: Intensité de buts de l'équipe à l'extérieur.
        rho: Paramètre de correction Dixon-Coles.
        max_goals: Nombre maximum de buts à considérer.

    Returns:
        Matrice (max_goals+1, max_goals+1) de probabilités.
    """
    # Squelette : à implémenter plus tard
    raise NotImplementedError
