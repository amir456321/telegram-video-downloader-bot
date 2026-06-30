from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def quality_keyboard(formats, cache_key):

    keyboard = []

    formats = sorted(
        formats,
        key=lambda x: x["height"],
        reverse=True,
    )

    for f in formats:

        keyboard.append([
            InlineKeyboardButton(
                f"🎬 {f['height']}p",
                callback_data=f"video:{cache_key}:{f['id']}"
            )
        ])

    keyboard.append([
        InlineKeyboardButton(
            "❌ لغو",
            callback_data=f"cancel:{cache_key}"
        )
    ])

    return InlineKeyboardMarkup(keyboard)
