import structlog
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from app.config.settings import settings

logger = structlog.get_logger()

bot = Bot(token=settings.telegram_bot_token)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("🧠 QFTE Bot démarré.
Envoie /help pour la liste des commandes.")


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = (
        "🧠 **QFTE Bot – Aide**

"
        "/start – Démarrer le bot
"
        "/help – Afficher cette aide

"
        "_Fonctionnalités à venir : /scan, /analyze, /tips, /stats, /risk, /audit_"
    )
    await message.answer(help_text, parse_mode="Markdown")


async def start_bot():
    logger.info("Démarrage du bot Telegram")
    await dp.start_polling(bot)
