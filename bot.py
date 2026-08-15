import logging
from aiohttp import web
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

from config import BOT_TOKEN, PORT
from handlers.start import start_command, button_callback_handler
from handlers.help import help_command, about_command
from handlers.image import handle_image
from handlers.admin import stats_command, broadcast_command

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def health_check(request):
    return web.Response(
        text="GoodyTreat Background Remover Bot is operational.",
        status=200,
    )


async def start_health_server():
    app = web.Application()
    app.router.add_get("/", health_check)
    app.router.add_get("/health", health_check)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    logger.info(
        f"Health check web server running on http://0.0.0.0:{PORT}"
    )


def main():
    application = (
        ApplicationBuilder().token(BOT_TOKEN).build()
    )

    # User Command Handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))

    # Admin Command Handlers
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(
        CommandHandler("broadcast", broadcast_command)
    )

    # Callback Query Handler
    application.add_handler(
        CallbackQueryHandler(button_callback_handler)
    )

    # Image Message Handlers
    application.add_handler(
        MessageHandler(
            filters.PHOTO | filters.Document.IMAGE, handle_image
        )
    )

    # Health check web server hook on startup
    application.post_init = lambda app: start_health_server()

    logger.info("Starting Telegram Bot Polling...")
    application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
