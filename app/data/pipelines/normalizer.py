"""
Normalisation des données (squelette).

Pour l’instant, ce module est un placeholder.
Il sera complété dans la Phase 1 (S2) pour :
- normaliser les dates (ISO, fuseaux)
- normaliser les noms d’équipes (ex: “Man United” → “Manchester United”)
- normaliser les formats de cotes
"""

from typing import Any


def normalize_match_data(data: dict[str, Any]) -> dict[str, Any]:
    """
    Normalise les données d’un match.

    Version v0 : retourne les données telles quelles.
    À améliorer dans S2.
    """
    return data


def normalize_odds_data(data: dict[str, Any]) -> dict[str, Any]:
    """
    Normalise les données de cotes.

    Version v0 : retourne les données telles quelles.
    À améliorer dans S2.
    """
    return data
