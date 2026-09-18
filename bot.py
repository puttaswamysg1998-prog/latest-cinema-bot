import logging
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import BOT_TOKEN, API_ID, API_HASH, SHORTENER_URL, SHORTENER_API

logging.basicConfig(level=logging.INFO)

app = Client(
    "VPLinkFileBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

def get_short_link(original_link):
    api_url = f"https://{SHORTENER_URL}/api?api={SHORTENER_API}&url={original_link}"
    try:
        response = requests.get(api_url).json()
        if response.get("status") == "success":
            return response.get("shortenedUrl")
    except Exception as e:
        print(f"Error: {e}")
    return original_link

@app.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def file_handler(client, message):
    sent_msg = await message.copy(chat_id=message.from_user.id)
    file_id = sent_msg.id

    bot_info = await client.get_me()
    raw_link = f"https://t.me/{bot_info.username}?start=file_{file_id}"

    short_link = get_short_link(raw_link)

    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("📥 Download File (Watch Ads)", url=short_link)]]
    )

    await message.reply_text(
        "✨ **ನಿಮ್ಮ ಫೈಲ್ ಶಾರ್ಟ್‌ಲಿಂಕ್ ಸಿದ್ಧವಾಗಿದೆ!**\n\nಕೆಳಗಿನ ಬಟನ್ ಕ್ಲಿಕ್ ಮಾಡಿ ಡೌನ್‌ಲೋಡ್ ಮಾಡಿಕೊಳ್ಳಿ:",
        reply_markup=reply_markup
    )

@app.on_message(filters.private & filters.command("start"))
async def start_handler(client, message):
    if len(message.command) > 1 and message.command[1].startswith("file_"):
        file_id = int(message.command[1].split("_")[1])
        await client.copy_message(
            chat_id=message.from_user.id,
            from_chat_id=message.from_user.id,
            message_id=file_id
        )
        return

    await message.reply_text("👋 ನಮಸ್ಕಾರ! ನನಗೆ ಯಾವುದೇ ಮೂವಿ ಅಥವಾ ಫೈಲ್ ಕಳುಹಿಸಿ, ನಾನು ನಿಮಗೆ VPLINK ಶಾರ್ಟ್‌ಲಿಂಕ್ ಸಿದ್ಧಪಡಿಸಿ ಕೊಡುತ್ತೇನೆ.")

print("Bot is running...")
app.run()
