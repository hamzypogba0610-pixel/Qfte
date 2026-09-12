# app/analysis/config.py
"""
Configuration globale du module d'analyse QFTE.
"""

# Mode : "production" ou "experimental"
# - production : seuls les modèles validés sont utilisés pour les notifs auto.
# - experimental : on peut tester de nouveaux modèles, mais pas de notif auto.
MODE = "production"

# Seuils pour les notifications automatiques (bot Telegram)
MIN_GLOBAL_CONFIDENCE_FOR_AUTO_POST = 8.5   # 0–10
MIN_EDGE_FOR_AUTO_POST = 0.05               # 5% d'edge minimum
MIN_STRONG_MARKETS_FOR_AUTO_POST = 3        # nb marchés avec confiance ≥ 7.5

# Seuil pour considérer un marché comme "fort"
CONFIDENCE_THRESHOLD_STRONG = 7.5

# Critères de sélection des "2 matchs fiables du jour"
# On classe par : global_confidence, puis edge, puis strong_markets_count.
TOP2_MIN_GLOBAL_CONFIDENCE = 6.0
TOP2_MIN_STRONG_MARKETS = 2

# Sports supportés
SUPPORTED_SPORTS = ["football", "basketball", "tennis"]

# Marchés obligatoires pour une analyse complète (par sport)
REQUIRED_MARKETS_BY_SPORT = {
    "football": ["1N2", "OU_2.5", "handicap", "btts", "score_ft"],
    "basketball": ["1N2", "OU_2.5", "handicap"],
    "tennis": ["1N2", "OU_2.5", "handicap"],
}
