from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from Unzip.config import AUTH_CHANNEL
from pyrogram.errors import UserNotParticipant

active_tasks = {}

async def is_subscribed(bot, query, channel):
    btn = []
    for id in channel:
        chat = await bot.get_chat(int(id))
        try:
            await bot.get_chat_member(id, query.from_user.id)
        except UserNotParticipant:
            btn.append([InlineKeyboardButton(f'Join channel', url=chat.invite_link)])
        except Exception as e:
            print(f"Error checking subscription for {id}: {e}")
    return btn

@Client.on_message(filters.command("start"))
async def start(client, message):
    if not AUTH_CHANNEL:
        await message.reply("No channels to subscribe to. Please check the configuration.")
        return

    try:
        btn = await is_subscribed(client, message, AUTH_CHANNEL)
        if btn:
            username = (await client.get_me()).username

            new_button = [InlineKeyboardButton("join channel ", url="https://t.me/JN2FLIX")]
            btn.insert(0, new_button)  # Adds the new button at the beginning of the list
    
            if len(message.command) > 1:
                btn.append([InlineKeyboardButton("♻️ Try Again ♻️", url=f"https://t.me/{username}?start={message.command[1]}")])
            else:
                btn.append([InlineKeyboardButton("♻️ Try Again ♻️", url=f"https://t.me/{username}?start=true")])
            await message.reply_text(text=f"<b>👋 Hello {message.from_user.mention},\n\nPlease join below 2 channel to use me\n\nafter join click ♻️ Try Again ♻️</b>", reply_markup=InlineKeyboardMarkup(btn))
            return
        else:
            await message.reply("You can now use the bot.")
    except Exception as e:
        print(e)

    reply_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("main update Channel", url="https://t.me/JN2FLIX"),
        ],
        [
            InlineKeyboardButton("bots Update Channel", url="https://t.me/ROCKERSBACKUP"),
        ] 
    ]
    )
    start_message = (
        "Hello!\n\n"
        "Send me a ZIP file, and I'll unzip it for you."
    )
    await message.reply(start_message, reply_markup=reply_markup)

# Callback query handler
@Client.on_callback_query(filters.regex("cancel"))
async def cancel(client, callback_query):
    await callback_query.message.delete()

@Client.on_message(filters.command("help"))
async def help_command(client, message):
    help_message = (
        "Here are the commands you can use:\n\n"
        "/start - Start the bot and get the welcome message\n"
        "/help - Get help on how to use the bot\n\n"
        "To unzip a file, simply send me a ZIP file and I will extract its contents and send them back to you.\n\n"
        "©️ Channel : @ROCKERSBACKUP @JN2FLIX"
    )
    await message.reply(help_message)

@Client.on_callback_query(filters.regex("cancel_unzip"))
async def cancel_callback(client, callback_query):
    user_id = callback_query.from_user.id

    if user_id in active_tasks:
        task = active_tasks[user_id]
        task.cancel()
        await callback_query.answer("⛔ Unzipping has been cancelled.", show_alert=True)
    else:
        await callback_query.answer("⚠️ No ongoing unzip operation.", show_alert=True)
