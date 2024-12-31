# ©️ LISA-KOREA | @LISA_FAN_LK | NT_BOT_CHANNEL | LISA-KOREA/UnZip-Bot

# [⚠️ Do not change this repo link ⚠️] :- https://github.com/LISA-KOREA/UnZip-Bot



from pyrogram import Client
from Unzip.config import config


app = Client(
    "unzip_bot",
    bot_token=config.BOT_TOKEN,
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    plugins=dict(root="Unzip")
)


print("🎊 I AM ALIVE 🎊  • Support @NT_BOTS_SUPPORT")
app.run()
