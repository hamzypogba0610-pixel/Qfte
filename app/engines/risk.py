# app/engines/risk.py
"""
Risk Engine pour QFTE.

Ce module fournit :
- Le calcul de la fraction de Kelly (full, half, quarter, etc.).
- La gestion de la bankroll (taille de mise, limites min/max).
- Un score de risque par pari.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class BankrollConfig:
    """
    Configuration de la bankroll et des limites de mise.
    """
    bankroll: float                # Bankroll totale actuelle
    kelly_fraction: float = 0.25   # Fraction de Kelly (0.25 = quarter-Kelly)
    min_stake: float = 1.0         # Mise minimale absolue
    max_stake: Optional[float] = None  # Mise maximale absolue (None = pas de limite)
    max_pct_bankroll: float = 0.05 # Mise max en % de la bankroll (ex: 5%)


def kelly_fraction_full(
    win_prob: float,
    decimal_odd: float,
) -> float:
    """
    Calcule la fraction de Kelly "pleine" pour un pari.

    Formule : f* = (b * p - q) / b
    où :
      - b = odd - 1 (gain net par unité mise)
      - p = probabilité de gain
      - q = 1 - p

    Args:
        win_prob: Probabilité de gain (0..1).
        decimal_odd: Cote décimale.

    Returns:
        Fraction de bankroll à miser (peut être négative = ne pas parier).
    """
    # Squelette : à implémenter plus tard
    raise NotImplementedError


def kelly_fraction_adjusted(
    win_prob: float,
    decimal_odd: float,
    kelly_fraction: float = 0.25,
) -> float:
    """
    Calcule la fraction de Kelly ajustée (fractionnée).

    Args:
        win_prob: Probabilité de gain (0..1).
        decimal_odd: Cote décimale.
        kelly_fraction: Fraction de Kelly (0.25 = quarter-Kelly, 0.5 = half-Kelly, etc.).

    Returns:
        Fraction de bankroll à miser (0 si Kelly négatif).
    """
    # Squelette : à implémenter plus tard
    raise NotImplementedError


def compute_stake(
    win_prob: float,
    decimal_odd: float,
    config: BankrollConfig,
) -> float:
    """
    Calcule la mise recommandée en fonction de Kelly et de la config.

    Règles :
    - Kelly fractionné → fraction de bankroll.
    - Applique min_stake, max_stake, max_pct_bankroll.
    - Si Kelly ≤ 0 → mise = 0.

    Args:
        win_prob: Probabilité de gain (0..1).
        decimal_odd: Cote décimale.
        config: BankrollConfig avec bankroll, fraction de Kelly, limites.

    Returns:
        Mise recommandée (0 si pas de pari).
    """
    # Squelette : à implémenter plus tard
    raise NotImplementedError


def risk_score(
    ev: float,
    kelly_frac: float,
    drs_score: Optional[float] = None,
) -> float:
    """
    Calcule un score de risque pour un pari (0..1).

    Plus le score est élevé, plus le pari est risqué.

    Args:
        ev: Expected value du pari.
        kelly_frac: Fraction de Kelly (0..1).
        drs_score: Score de confiance data (0..1), optionnel.

    Returns:
        Score de risque (0..1).
    """
    # Squelette : à implémenter plus tard
    raise NotImplementedError
