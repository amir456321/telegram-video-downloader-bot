from telegram import Update
from telegram.ext import ContextTypes

from keyboards.quality import quality_keyboard
from services.cache import cache
from services.ytdlp import YTDLP


async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if not url.startswith(("http://", "https://")):
        await update.message.reply_text("❌ لینک معتبر نیست")
        return

    try:
        ytdlp = YTDLP()

        info = ytdlp.info(url)
        formats = ytdlp.formats(url)

        title = info.get("title", "Unknown")
        duration = info.get("duration", 0)
        uploader = info.get("uploader", "Unknown")

        cache_key = cache.create({
            "url": url,
            "title": title,
        })

        await update.message.reply_text(
            f"🎬 {title}\n"
            f"👤 {uploader}\n"
            f"⏱ {duration} ثانیه\n\n"
            f"کیفیت موردنظر را انتخاب کن:",
            reply_markup=quality_keyboard(formats, cache_key),
        )

    except Exception as e:
        await update.message.reply_text(f"❌ خطا:\n{e}")
