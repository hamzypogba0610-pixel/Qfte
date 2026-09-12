# scripts/run_bot.py
"""
Point d'entrée pour lancer le bot Telegram QFTE.

Utilisation :
    python scripts/run_bot.py
"""

import sys
from pathlib import Path

# Ajouter la racine du projet au PYTHONPATH
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from bot.telegram_bot import main


if __name__ == "__main__":
    main()
