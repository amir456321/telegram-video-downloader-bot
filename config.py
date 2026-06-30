import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

DOWNLOAD_DIR = "/tmp/telegram-downloader"

MAX_FILE_SIZE = 2 * 1024 * 1024 * 1024  # 2GB
