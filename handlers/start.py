from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import db


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await db.add_user(
        user.id, user.username or user.first_name or "Unknown"
    )

    welcome_text = (
        f"👋 **Hello, {user.first_name}!**\n\n"
        "Welcome to **GoodyTreat Background Remover** (@goodytreatbot)!\n"
        "I can remove the background from any photo automatically and return a clean transparent PNG.\n\n"
        "🖼 **How to Use:**\n"
        "Simply send or forward any image to this chat as a **Photo** or **File/Document**.\n\n"
        "⚡️ **Supported Formats:** JPG, JPEG, PNG, WEBP\n\n"
        "Tap a button below to explore or get started immediately!"
    )

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🖼 Remove Background",
                    callback_data="btn_remove_info",
                )
            ],
            [
                InlineKeyboardButton(
                    "ℹ️ Help", callback_data="btn_help"
                ),
                InlineKeyboardButton(
                    "👨‍💻 About", callback_data="btn_about"
                ),
            ],
        ]
    )

    await update.message.reply_text(
        welcome_text, parse_mode="Markdown", reply_markup=keyboard
    )


async def button_callback_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    if query.data == "btn_remove_info":
        await query.message.reply_text(
            "📥 **Ready!** Send or upload an image now to remove its background."
        )
    elif query.data == "btn_help":
        from handlers.help import get_help_text

        await query.message.reply_text(
            get_help_text(), parse_mode="Markdown"
        )
    elif query.data == "btn_about":
        from handlers.help import get_about_text

        await query.message.reply_text(
            get_about_text(), parse_mode="Markdown"
        )
