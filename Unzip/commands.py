from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Unzip.config import AUTH_CHANNEL
from pymongo import MongoClient
from pyrogram.errors import UserNotParticipant
import time

# MongoDB connection setup
client = MongoClient("mongodb+srv://telegram:telegram@cluster0.ubgb2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")  # Replace with your MongoDB URL
db = client["unzip_bot"]  # Database name
users_collection = db["users"]  # Collection to store user data

# Function to get all user IDs from MongoDB
def get_all_user_ids():
    users = users_collection.find({}, {"_id": 0, "user_id": 1})
    return [user["user_id"] for user in users]

# Function to add a new user ID to MongoDB
def add_user_id(user_id):
    if not users_collection.find_one({"user_id": user_id}):
        users_collection.insert_one({"user_id": user_id})

# Function to check subscription
async def is_subscribed(bot, query, channel):
    btn = []
    for id in channel:
        chat = await bot.get_chat(int(id))
        try:
            await bot.get_chat_member(id, query.from_user.id)
        except UserNotParticipant:
            btn.append([InlineKeyboardButton(f'Join channel', url=chat.invite_link)] )
        except Exception as e:
            print(f"Error checking subscription for {id}: {e}")
    return btn

# Command to track new users and handle subscription
@Client.on_message(filters.command("start"))
async def start(client, message):
    if not AUTH_CHANNEL:
        await message.reply("No channels to subscribe to. Please check the configuration.")
        return

    try:
        btn = await is_subscribed(client, message, AUTH_CHANNEL)
        if btn:
            username = (await client.get_me()).username
            new_button = [InlineKeyboardButton("Join Channel", url="https://t.me/JN2FLIX")]
            btn.insert(0, new_button)  # Adds the new button at the beginning of the list
    
            if len(message.command) > 1:
                btn.append([InlineKeyboardButton("♻️ Try Again ♻️", url=f"https://t.me/{username}?start={message.command[1]}")])
            else:
                btn.append([InlineKeyboardButton("♻️ Try Again ♻️", url=f"https://t.me/{username}?start=true")])
            await message.reply_text(text=f"<b>👋 Hello {message.from_user.mention},\n\nPlease join below 2 channels to use me\n\nAfter joining, click ♻️ Try Again ♻️</b>", reply_markup=InlineKeyboardMarkup(btn))
            return
        else:
            await message.reply("You can now use the bot.")
    except Exception as e:
        print(e)

    reply_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Main Update Channel", url="https://t.me/JN2FLIX"),
        ],
        [
            InlineKeyboardButton("Bots Update Channel", url="https://t.me/ROCKERSBACKUP"),
        ] 
    ]
    )
    start_message = (
        "Hello!\n\n"
        "Send me a ZIP file, and I'll unzip it for you."
    )
    await message.reply(start_message, reply_markup=reply_markup)

# Broadcast command handler
@Client.on_message(filters.command("broadcast") & filters.user(6643562770))  # Replace with your OWNER_ID
async def broadcast(client, message):
    if len(message.command) < 2:
        await message.reply("Please provide a message to broadcast.")
        return

    broadcast_message = message.text.split(None, 1)[1]
    
    # Get the list of user IDs to send the broadcast message to
    user_ids = get_all_user_ids()

    total_users = len(user_ids)
    current = 0

    # Send the broadcast message to all users
    start_time = time.time()
    progress_message = await message.reply("Starting broadcast...")

    for user_id in user_ids:
        try:
            await client.send_message(user_id, broadcast_message)
            current += 1
            await broadcast_progress(current, total_users, progress_message, start_time)
        except Exception as e:
            print(f"Failed to send message to {user_id}: {e}")

    await progress_message.edit("✅ Broadcast completed.")

# Function to display broadcast progress
async def broadcast_progress(current, total, message, start_time):
    progress = (current / total) * 100
    elapsed_time = time.time() - start_time
    remaining_time = elapsed_time / current * (total - current) if current > 0 else 0
    remaining_time_str = str(int(remaining_time)) + "s" if remaining_time > 0 else "Calculating..."
    
    progress_message = f"Broadcast Progress: {current}/{total} sent\nTime remaining: {remaining_time_str}\n{progress:.2f}%"
    
    # Update the message with progress
    await message.edit(progress_message)

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
