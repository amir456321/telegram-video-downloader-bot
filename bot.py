import os
from dotenv import load_dotenv
import yt_dlp
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    try:
        ydl_opts = {
            "format": "best",
            "outtmpl": "downloads/%(title)s.%(ext)s",
        }

        os.makedirs("downloads", exist_ok=True)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        await update.message.reply_video(video=open(filename, "rb"))

        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(str(e))

app = Application.builder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT, download))

app.run_polling()
