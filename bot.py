from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

from config import BOT_TOKEN
from handlers.start import start
from handlers.download import download
from handlers.callbacks import callbacks
from services.updater import start_updater


def main():

    # اجرای آپدیت خودکار yt-dlp در پس‌زمینه
    start_updater()

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            download,
        )
    )
    app.add_handler(CallbackQueryHandler(callbacks))

    print("🤖 Bot Started")

    app.run_polling()


if __name__ == "__main__":
    main()
