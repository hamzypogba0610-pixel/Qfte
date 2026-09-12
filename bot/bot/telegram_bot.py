# bot/telegram_bot.py
"""
Bot Telegram privé QFTE – interface utilisateur pour les analyses de matchs.
"""

import logging
from typing import Any, Dict, List

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

from bot import config
from bot import messages
from app.analysis import predictor, selector, types


# -------------------------
# Logging
# -------------------------
logging.basicConfig(
    format="%(asctime)s – %(name)s – %(levelname)s – %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# -------------------------
# Helpers
# -------------------------
def _check_user_allowed(update: Update) -> bool:
    """
    Vérifie que l'utilisateur qui parle au bot est bien celui autorisé (TELEGRAM_USER_ID).
    """
    if update.effective_user is None:
        return False
    return update.effective_user.id == config.TELEGRAM_USER_ID


def _dummy_matches_today(sport: str | None = None) -> List[Dict[str, Any]]:
    """
    Génère une liste de matchs "fictifs" pour illustrer /today, /next, /live.
    À remplacer plus tard par un vrai fetch de données.
    """
    base_matches = [
        {
            "sport": "football",
            "competition": "Ligue 1",
            "home": "PSG",
            "away": "OM",
            "start_time": "2026-09-15T21:00:00",
            "is_live": False,
            "score_current": None,
            "minute": None,
        },
        {
            "sport": "basketball",
            "competition": "NBA",
            "home": "Lakers",
            "away": "Celtics",
            "start_time": "2026-09-15T02:00:00",
            "is_live": False,
            "score_current": None,
            "minute": None,
        },
        {
            "sport": "tennis",
            "competition": "ATP – Tournoi X",
            "home": "Joueur A",
            "away": "Joueur B",
            "start_time": "2026-09-15T14:30:00",
            "is_live": False,
            "score_current": None,
            "minute": None,
        },
        {
            "sport": "football",
            "competition": "Premier League",
            "home": "Arsenal",
            "away": "Chelsea",
            "start_time": "2026-09-15T18:30:00",
            "is_live": True,
            "score_current": "1-0",
            "minute": "32'",
        },
    ]

    if sport:
        return [m for m in base_matches if m["sport"] == sport]
    return base_matches


# -------------------------
# Command handlers
# -------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Gestion de /start
    """
    if not _check_user_allowed(update):
        await update.message.reply_text("Accès non autorisé.")
        return

    text = (
        "Bienvenue sur le bot QFTE v22 ⚽🏀🎾

"
        "Je suis ton assistant personnel d'analyse de matchs.
"
        "Je peux analyser des matchs de football, basketball et tennis, "
        "en pré-live et en live, avec :
"
        "- 1N2 / vainqueur
"
        "- Over/Under 1.5 / 2.5 / 3.5
"
        "- Handicap
"
        "- BTTS (football)
"
        "- Scores HT / FT

"
        "Commandes principales :
"
        "- /help : voir l'aide
"
        "- /today : matchs du jour
"
        "- /next : matchs à venir
"
        "- /live : matchs en cours
"
        "- /analyse Équipe1 Équipe2 : analyse complète d'un match
"
        "- /top2 : les 2 matchs les plus fiables du jour

"
        "Tout est basé sur la méthodologie QFTE (modèles + calibration + backtest)."
    )

    await update.message.reply_text(text)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Gestion de /help
    """
    if not _check_user_allowed(update):
        await update.message.reply_text("Accès non autorisé.")
        return

    text = (
        "📘 Aide – Bot QFTE v22

"
        "Commandes disponibles :
"
        "- /start : message de bienvenue
"
        "- /today : liste des matchs du jour (foot, basket, tennis)
"
        "- /next : matchs des prochaines 24–48h
"
        "- /live : matchs en cours
"
        "- /analyse Équipe1 Équipe2 : analyse complète d'un match
"
        "- /top2 : les 2 matchs les plus fiables du jour selon QFTE

"
        "Exemple :
"
        "/analyse PSG OM
"
        "/analyse Lakers Celtics

"
        "Le bot t'enverra aussi automatiquement les opportunités les plus fortes "
        "(confiance élevée, edge important)."
    )

    await update.message.reply_text(text)


async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Gestion de /today
    """
    if not _check_user_allowed(update):
        await update.message.reply_text("Accès non autorisé.")
        return

    matches = _dummy_matches_today()
    text = messages.format_match_list(matches, "Matchs du jour")
    await update.message.reply_text(text)


async def next_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Gestion de /next
    """
    if not _check_user_allowed(update):
        await update.message.reply_text("Accès non autorisé.")
        return

    matches = _dummy_matches_today()  # à remplacer par vrais matchs à venir
    text = messages.format_match_list(matches, "Matchs à venir (24–48h)")
    await update.message.reply_text(text)


async def live(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Gestion de /live
    """
    if not _check_user_allowed(update):
        await update.message.reply_text("Accès non autorisé.")
        return

    all_matches = _dummy_matches_today()
    live_matches = [m for m in all_matches if m.get("is_live", False)]
    text = messages.format_match_list(live_matches, "Matchs en live")
    await update.message.reply_text(text)


async def analyse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Gestion de /analyse Équipe1 Équipe2
    """
    if not _check_user_allowed(update):
        await update.message.reply_text("Accès non autorisé.")
        return

    args = context.args  # liste des mots après /analyse
    if len(args) < 2:
        await update.message.reply_text(
            "Utilisation : /analyse Équipe1 Équipe2
Exemple : /analyse PSG OM"
        )
        return

    home = args
    away = args[1]

    # Pour l'instant, on simule un match de football
    # Plus tard : détection du sport, récupération des vraies données, etc.
    match_data = {
        "competition": "Compétition X",
        "home": home,
        "away": away,
        "start_time": "2026-09-15T21:00:00",
    }

    # Analyse pré-live (placeholder)
    analysis = predictor.analyze_match_pre_live(match_data, "football")

    text = messages.format_match_analysis(analysis)
    await update.message.reply_text(text)


async def top2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Gestion de /top2
    """
    if not _check_user_allowed(update):
        await update.message.reply_text("Accès non autorisé.")
        return

    # Pour l'instant, on utilise les matchs fictifs
    matches = _dummy_matches_today()

    analyses: List[types.MatchAnalysis] = []
    for m in matches:
        match_data = {
            "competition": m["competition"],
            "home": m["home"],
            "away": m["away"],
            "start_time": m["start_time"],
        }
        analysis = predictor.analyze_match_pre_live(match_data, m["sport"])
        analyses.append(analysis)

    top2_analyses = selector.select_top2_matches(analyses)
    text = messages.format_top2_matches(top2_analyses)
    await update.message.reply_text(text)


# -------------------------
# Notifications automatiques (squelette)
# -------------------------
async def send_auto_alerts(application: Application):
    """
    Fonction appelée périodiquement (ex. : toutes les heures) pour envoyer
    des alertes automatiques sur les opportunités fortes.

    Pour l'instant, c'est un squelette : on utilise les mêmes matchs fictifs.
    À connecter plus tard à un vrai scheduler (APScheduler, cron, etc.).
    """
    if config.MODE != "production":
        return

    matches = _dummy_matches_today()
    analyses: List[types.MatchAnalysis] = []

    for m in matches:
        match_data = {
            "competition": m["competition"],
            "home": m["home"],
            "away": m["away"],
            "start_time": m["start_time"],
        }
        analysis = predictor.analyze_match_pre_live(match_data, m["sport"])
        analyses.append(analysis)

    # Filtrer les opportunités fortes
    strong = [
        a for a in analyses
        if a.global_confidence >= config.MIN_GLOBAL_CONFIDENCE_FOR_AUTO_POST
        and a.edge >= config.MIN_EDGE_FOR_AUTO_POST
        and a.strong_markets_count >= config.MIN_STRONG_MARKETS_FOR_AUTO_POST
    ]

    if not strong:
        return

    for a in strong:
        text = messages.format_auto_alert(a)
        try:
            await application.bot.send_message(
                chat_id=config.TELEGRAM_USER_ID,
                text=text,
            )
        except Exception as e:
            logger.error(f"Erreur envoi alerte auto : {e}")


# -------------------------
# Main
# -------------------------
def main():
    """
    Point d'entrée principal du bot.
    """
    if config.TELEGRAM_BOT_TOKEN == "TON_TOKEN_ICI":
        raise RuntimeError(
            "Tu dois configurer TELEGRAM_BOT_TOKEN dans bot/config.py "
            "(token obtenu via @BotFather)."
        )
    if config.TELEGRAM_USER_ID == 0:
        raise RuntimeError(
            "Tu dois configurer TELEGRAM_USER_ID dans bot/config.py "
            "(ton user ID Telegram)."
        )

    application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()

    # Commandes
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("today", today))
    application.add_handler(CommandHandler("next", next_command))
    application.add_handler(CommandHandler("live", live))
    application.add_handler(CommandHandler("analyse", analyse))
    application.add_handler(CommandHandler("top2", top2))

    # Ici, plus tard : ajouter un job scheduler pour send_auto_alerts

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
