"""
Provider API-Football (squelette).

Pour l’instant, ce module est un placeholder.
Il sera complété dans la Phase 1 (S2) pour :
- appeler l’API-Football (fixtures, results, odds)
- normaliser les données
- les renvoyer sous forme de dicts / modèles Pydantic
"""

from app.config.settings import settings


class FootballProvider:
    def __init__(self):
        self.api_key = getattr(settings, "api_football_key", "")
        self.base_url = "[https://v3.football.api-sports.io](https://v3.football.api-sports.io)"

    async def get_fixtures(self, league: str, season: str):
        # TODO: appeler API-Football et retourner les fixtures
        raise NotImplementedError("À implémenter dans S2")

    async def get_results(self, league: str, season: str):
        # TODO: appeler API-Football et retourner les résultats
        raise NotImplementedError("À implémenter dans S2")

    async def get_odds(self, match_id: str):
        # TODO: appeler API-Football et retourner les cotes
        raise NotImplementedError("À implémenter dans S2")
