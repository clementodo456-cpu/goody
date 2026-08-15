import logging
from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_ID
from database import db

logger = logging.getLogger(__name__)


def is_admin(user_id: int) -> bool:
    return ADMIN_ID is not None and user_id == ADMIN_ID


async def stats_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        return

    stats = await db.get_stats()

    stats_text = (
        "📊 **Bot Operational Statistics**\n\n"
        f"👥 **Total Users:** `{stats['total_users']}`\n"
        f"🖼 **Total Images Received:** `{stats['images_processed']}`\n"
        f"✅ **Successful Operations:** `{stats['successful_ops']}`\n"
        f"❌ **Failed Operations:** `{stats['failed_ops']}`"
    )

    await update.message.reply_text(stats_text, parse_mode="Markdown")


async def broadcast_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        return

    if not context.args:
        await update.message.reply_text(
            "⚠️ **Usage:** `/broadcast Your message text here`",
            parse_mode="Markdown",
        )
        return

    broadcast_msg = " ".join(context.args)
    user_ids = await db.get_all_user_ids()

    success_count = 0
    fail_count = 0

    await update.message.reply_text(
        f"🚀 Starting broadcast to {len(user_ids)} users..."
    )

    for uid in user_ids:
        try:
            await context.bot.send_message(
                chat_id=uid,
                text=f"📢 **Announcement**\n\n{broadcast_msg}",
                parse_mode="Markdown",
            )
            success_count += 1
        except Exception as e:
            logger.warning(
                f"Failed to send broadcast to user {uid}: {e}"
            )
            fail_count += 1

    await update.message.reply_text(
        f"✅ **Broadcast Completed!**\n\n"
        f"• Success: `{success_count}`\n"
        f"• Failed: `{fail_count}`",
        parse_mode="Markdown",
    )
