"""
Script de seed de la base de données.

Pour l’instant, c’est un squelette.
Il sera complété dans la Phase 1 (S2) pour :
- appeler API-Football
- insérer fixtures, results, odds
- calculer un DRS v0
"""

import asyncio
from app.config.settings import settings
from app.database.session import engine


async def seed_db():
    print("Seed DB (squelette) – à compléter")
    print(f"DB URL: {settings.database_url}")


async def main():
    await seed_db()


if __name__ == "__main__":
    asyncio.run(main())
