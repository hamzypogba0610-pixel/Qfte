# bot/config.py
"""
Configuration du bot Telegram QFTE.
"""

# -------------------------
# Telegram
# -------------------------
# À remplacer par ton vrai token obtenu via @BotFather
TELEGRAM_BOT_TOKEN = ""

# Ton user ID Telegram (le bot est privé, un seul utilisateur)
# Tu peux l'obtenir avec des bots comme @userinfobot ou @getmyid_bot
TELEGRAM_USER_ID =8732639465  # remplace 0 par ton vrai user ID (int)

# -------------------------
# Comportement du bot
# -------------------------
# Langue du bot
LANGUAGE = "fr"

# Mode : "production" ou "experimental"
# - production : notifications auto selon les seuils ci-dessous
# - experimental : pas de notif auto, juste réponses aux commandes
MODE = "production"

# -------------------------
# Seuils pour notifications automatiques
# -------------------------
# Ces seuils doivent être cohérents avec app/analysis/config.py
MIN_GLOBAL_CONFIDENCE_FOR_AUTO_POST = 8.5   # 0–10
MIN_EDGE_FOR_AUTO_POST = 0.05               # 5%
MIN_STRONG_MARKETS_FOR_AUTO_POST = 3        # nb marchés avec confiance ≥ 7.5

# -------------------------
# Commandes activées
# -------------------------
ENABLE_COMMANDS = {
    "start": True,
    "help": True,
    "today": True,
    "next": True,
    "live": True,
    "analyse": True,
    "top2": True,
    "stats": False,  # à activer plus tard
}
