import os
import sys
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    sys.exit("CRITICAL ERROR: BOT_TOKEN is missing in environment variables.")

ADMIN_ID_RAW = os.getenv("ADMIN_ID", "")
ADMIN_ID = int(ADMIN_ID_RAW) if ADMIN_ID_RAW.isdigit() else None

REMOVEBG_API_KEY = os.getenv("REMOVEBG_API_KEY", "").strip()
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "20"))
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
PORT = int(os.getenv("PORT", "8080"))

ALLOWED_MIME_TYPES = ["image/jpeg", "image/png", "image/webp"]
ALLOWED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".webp"]
