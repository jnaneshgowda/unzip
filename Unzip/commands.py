# ©️ LISA-KOREA | @LISA_FAN_LK | NT_BOT_CHANNEL | LISA-KOREA/UnZip-Bot
# [⚠️ Do not change this repo link ⚠️] :- https://github.com/LISA-KOREA/UnZip-Bot

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from Config import Config

active_tasks = {}

# Function to check if a user is subscribed to all required channels
async def is_subscribed(client, user_id):
    for channel_id in Config.FORCE_SUB_CHANNELS:
        try:
            user_status = await client.get_chat_member(channel_id, user_id)
            if user_status.status not in ["member", "administrator", "creator"]:
                return False
        except Exception:
            return False
    return True


@Client.on_message(filters.command("start"))
async def start(client, message):
    user_id = message.from_user.id

    # Check if the user is subscribed
    if not await is_subscribed(client, user_id):
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("📍 Join Channel 1", url="https://t.me/NT_BOT_CHANNEL"),
                ],
                [
                    InlineKeyboardButton("📍 Join Channel 2", url="https://t.me/Another_Channel"),
                ],
            ]
        )
        await message.reply(
            "⚠️ To use this bot, you must join our channels first.\n\n"
            "👉 [Channel 1](https://t.me/NT_BOT_CHANNEL)\n"
            "👉 [Channel 2](https://t.me/Another_Channel)\n\n"
            "After joining, press /start again.",
            reply_markup=reply_markup,
            disable_web_page_preview=True,
        )
        return

    # If subscribed, send the start message
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("📍 Update Channel", url="https://t.me/NT_BOT_CHANNEL"),
            ],
            [
                InlineKeyboardButton("👥 Support Group", url="https://t.me/NT_BOTS_SUPPORT"),
                InlineKeyboardButton("👩‍💻 Developer", url="https://t.me/LISA_FAN_LK"),
            ],
        ]
    )
    start_message = (
        "Hello!\n\n"
        "Send me a ZIP file, and I'll unzip it for you."
    )
    await message.reply(start_message, reply_markup=reply_markup)


@Client.on_message(filters.command("help"))
async def help_command(client, message):
    user_id = message.from_user.id

    # Check if the user is subscribed
    if not await is_subscribed(client, user_id):
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("📍 Join Channel 1", url="https://t.me/NT_BOT_CHANNEL"),
                ],
                [
                    InlineKeyboardButton("📍 Join Channel 2", url="https://t.me/Another_Channel"),
                ],
            ]
        )
        await message.reply(
            "⚠️ To use this bot, you must join our channels first.\n\n"
            "👉 [Channel 1](https://t.me/NT_BOT_CHANNEL)\n"
            "👉 [Channel 2](https://t.me/Another_Channel)\n\n"
            "After joining, press /help again.",
            reply_markup=reply_markup,
            disable_web_page_preview=True,
        )
        return

    # If subscribed, send the help message
    help_message = (
        "Here are the commands you can use:\n\n"
        "/start - Start the bot and get the welcome message\n"
        "/help - Get help on how to use the bot\n\n"
        "To unzip a file, simply send me a ZIP file and I will extract its contents and send them back to you.\n\n"
        "©️ Channel : @NT_BOT_CHANNEL"
    )
    await message.reply(help_message)


@Client.on_callback_query(filters.regex("cancel"))
async def cancel(client, callback_query):
    await callback_query.message.delete()


@Client.on_callback_query(filters.regex("cancel_unzip"))
async def cancel_callback(client, callback_query):
    user_id = callback_query.from_user.id

    if user_id in active_tasks:
        task = active_tasks[user_id]
        task.cancel()
        await callback_query.answer("⛔ Unzipping has been cancelled.", show_alert=True)
    else:
        await callback_query.answer("⚠️ No ongoing unzip operation.", show_alert=True)
