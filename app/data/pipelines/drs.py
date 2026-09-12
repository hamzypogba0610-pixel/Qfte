"""
DRS – Data Reliability Score (version v0, squelette).

Pour l’instant, ce module est un placeholder.
Il sera complété dans la Phase 1 (S2) pour :
- calculer un score de fiabilité par feature
- prendre en compte sample size, source reliability, stabilité temporelle
- renvoyer un DRS global (0–100)
"""

from typing import Any


def calculate_drs_v0(data: dict[str, Any], sample_size: int) -> float:
    """
    Version v0 du DRS.

    Pour l’instant, retourne un score basique basé sur sample_size.
    À améliorer dans S2.
    """
    if sample_size < 5:
        return 30.0
    elif sample_size < 15:
        return 60.0
    else:
        return 90.0
