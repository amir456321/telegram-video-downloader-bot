import os

from telegram import Update
from telegram.ext import ContextTypes

from database.cache import get_file_id, save_file_id
from services.cache import cache
from services.downloader import Downloader


async def callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data.startswith("cancel:"):
        key = data.split(":")[1]
        cache.delete(key)
        await query.edit_message_text("❌ عملیات لغو شد.")
        return

    if not data.startswith("video:"):
        return

    _, key, format_id = data.split(":", 2)

    item = cache.get(key)

    if not item:
        await query.edit_message_text(
            "❌ درخواست منقضی شده است. دوباره لینک را ارسال کنید."
        )
        return

    url = item["url"]

    # ابتدا بررسی می‌کنیم قبلاً این کیفیت دانلود شده یا نه
    file_id = get_file_id(url, format_id)

    if file_id:
        await query.edit_message_text("⚡ ارسال از کش تلگرام...")

        await context.bot.send_video(
            chat_id=query.message.chat.id,
            video=file_id,
            supports_streaming=True,
        )

        cache.delete(key)
        return

    await query.edit_message_text("⏳ در حال دانلود...")

    try:
        downloader = Downloader()

        filename = downloader.download(url, format_id)

        with open(filename, "rb") as video:

            message = await context.bot.send_video(
                chat_id=query.message.chat.id,
                video=video,
                supports_streaming=True,
            )

        # ذخیره file_id برای دفعات بعد
        save_file_id(
            url=url,
            quality=format_id,
            file_id=message.video.file_id,
        )

        if os.path.exists(filename):
            os.remove(filename)

        cache.delete(key)

    except Exception as e:

        await context.bot.send_message(
            chat_id=query.message.chat.id,
            text=f"❌ خطا:\n{e}"
        )
