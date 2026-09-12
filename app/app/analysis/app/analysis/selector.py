# app/analysis/selector.py
"""
Sélection des meilleurs matchs du jour selon la méthodologie QFTE.
"""

from typing import List
from .types import MatchAnalysis
from . import config


def select_top2_matches(analyses: List[MatchAnalysis]) -> List[MatchAnalysis]:
    """
    Sélectionne les 2 matchs les plus fiables parmi une liste d'analyses.

    Critères :
      - global_confidence >= TOP2_MIN_GLOBAL_CONFIDENCE
      - strong_markets_count >= TOP2_MIN_STRONG_MARKETS
      - tri par : global_confidence (desc), edge (desc), strong_markets_count (desc)
    """
    # Filtrage initial
    filtered = [
        a for a in analyses
        if a.global_confidence >= config.TOP2_MIN_GLOBAL_CONFIDENCE
        and a.strong_markets_count >= config.TOP2_MIN_STRONG_MARKETS
    ]

    if len(filtered) <= 2:
        return filtered

    # Tri
    sorted_analyses = sorted(
        filtered,
        key=lambda a: (
            a.global_confidence,
            a.edge,
            a.strong_markets_count,
        ),
        reverse=True,
    )

    return sorted_analyses[:2]
