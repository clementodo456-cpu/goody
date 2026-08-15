import os
import logging
from PIL import Image
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import (
    MAX_FILE_SIZE_BYTES,
    MAX_FILE_SIZE_MB,
    ALLOWED_EXTENSIONS,
)
from database import db
from services.bg_remover import BackgroundRemoverService
from utils.helpers import (
    get_temp_filename,
    cleanup_files,
    acquire_user_lock,
    release_user_lock,
)

logger = logging.getLogger(__name__)


async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.message

    file_obj = None
    file_name = "image.jpg"
    file_size = 0

    if message.photo:
        photo = message.photo[-1]
        file_obj = await context.bot.get_file(photo.file_id)
        file_size = photo.file_size or 0
        file_name = f"{photo.file_unique_id}.jpg"
    elif message.document:
        doc = message.document
        file_ext = os.path.splitext(doc.file_name or "")[1].lower()

        if file_ext not in ALLOWED_EXTENSIONS:
            await message.reply_text(
                f"❌ **Unsupported file extension!**\n\n"
                f"Accepted formats: `{', '.join(ALLOWED_EXTENSIONS)}`",
                parse_mode="Markdown",
            )
            return

        file_obj = await context.bot.get_file(doc.file_id)
        file_size = doc.file_size or 0
        file_name = doc.file_name or "image.png"
    else:
        return

    if file_size > MAX_FILE_SIZE_BYTES:
        await message.reply_text(
            f"⚠️ **File too large!**\n"
            f"Maximum allowed size is **{MAX_FILE_SIZE_MB} MB**. Please choose a smaller image.",
            parse_mode="Markdown",
        )
        return

    if not acquire_user_lock(user.id):
        await message.reply_text(
            "⏳ You already have an active image being processed. Please wait until it completes."
        )
        return

    status_msg = await message.reply_text(
        "⏳ **Removing background... Please wait.**", parse_mode="Markdown"
    )

    input_path = get_temp_filename(
        os.path.splitext(file_name)[1] or ".jpg"
    )
    output_path = get_temp_filename(".png")

    try:
        await file_obj.download_to_drive(input_path)

        try:
            with Image.open(input_path) as img:
                img.verify()
        except Exception:
            await status_msg.edit_text(
                "❌ **Invalid file format.** The file uploaded is corrupted or not a valid image."
            )
            await db.increment_metric("failed_ops")
            return

        await db.increment_metric("images_processed")

        success = await BackgroundRemoverService.process_image(
            input_path, output_path
        )

        if success and os.path.exists(output_path):
            await db.increment_metric("successful_ops")
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔄 Remove Another",
                            callback_data="btn_remove_info",
                        )
                    ]
                ]
            )

            with open(output_path, "rb") as out_file:
                await message.reply_document(
                    document=out_file,
                    filename="background_removed.png",
                    caption="✅ **Background removed successfully!**",
                    parse_mode="Markdown",
                    reply_markup=keyboard,
                )
            await status_msg.delete()
        else:
            await db.increment_metric("failed_ops")
            await status_msg.edit_text(
                "❌ **Background removal failed.** Could not separate background. Please try another image."
            )

    except Exception as e:
        logger.error(
            f"Error processing image for user {user.id}: {e}",
            exc_info=True,
        )
        await db.increment_metric("failed_ops")
        await status_msg.edit_text(
            "⚠️ **An unexpected error occurred** while processing your image. Please try again later."
        )
    finally:
        release_user_lock(user.id)
        cleanup_files(input_path, output_path)
