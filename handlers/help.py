from telegram import Update
from telegram.ext import ContextTypes


def get_help_text() -> str:
    return (
        "📖 **GoodyTreat Bot Help Guide**\n\n"
        "1️⃣ **Sending Images:**\n"
        "• Send any photo as a standard picture or attachment file.\n"
        "• Supported Formats: `.jpg`, `.jpeg`, `.png`, `.webp`.\n"
        "• Max File Size: Up to 20 MB.\n\n"
        "2️⃣ **Processing Steps:**\n"
        "• Upload photo ➔ Wait a few seconds ➔ Receive transparent PNG.\n\n"
        "3️⃣ **Troubleshooting:**\n"
        "• If background removal fails, ensure the subject has clear contrast with the background.\n"
        "• Ensure your file does not exceed size limits.\n"
        "• Try sending as an uncompressed document if compressed photos fail."
    )


def get_about_text() -> str:
    return (
        "👨‍💻 **About GoodyTreat Background Remover**\n\n"
        "@goodytreatbot is an automated utility built using Python, `python-telegram-bot`, "
        "and advanced background separation tools.\n\n"
        "🔒 **Privacy First:**\n"
        "Images are processed in memory / isolated temporary disk storage and immediately deleted "
        "after processing. Your files are never stored or shared.\n\n"
        "✨ **Version:** 1.0.0 (Production-Ready)"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_help_text(), parse_mode="Markdown")


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        get_about_text(), parse_mode="Markdown"
    )
