"""
Feature Store (squelette).

Pour l’instant, ce module est un placeholder.
Il sera complété dans la Phase 1 (S2) pour :
- stocker les features par match/équipe
- versionner les features
- permettre des snapshots (T-24h, T-1h, etc.)
"""

from typing import Any


class FeatureStore:
    def __init__(self):
        # TODO: connecter à la DB
        pass

    async def save_features(self, match_id: str, features: dict[str, Any]):
        """
        Sauvegarde les features d’un match.

        Version v0 : ne fait rien.
        À améliorer dans S2.
        """
        pass

    async def get_features(self, match_id: str) -> dict[str, Any]:
        """
        Récupère les features d’un match.

        Version v0 : retourne un dict vide.
        À améliorer dans S2.
        """
        return {}
