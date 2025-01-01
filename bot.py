import time  # Add this import at the top of your file
from pymongo import MongoClient
from pyrogram import Client, filters
from Unzip.config import config
import asyncio

# MongoDB connection setup
client = MongoClient("mongodb+srv://telegram:telegram@cluster0.ubgb2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")  # Replace with your MongoDB URL
db = client["unzip_bot"]  # Database name
users_collection = db["users"]  # Collection to store user data

# Initialize the bot client
app = Client(
    "unzip_bot",
    bot_token=config.BOT_TOKEN,
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    plugins=dict(root="Unzip")
)

# Replace with your user ID
OWNER_ID = 6643562770  # Your user ID here

# Function to get all user IDs from MongoDB
def get_all_user_ids():
    users = users_collection.find({}, {"_id": 0, "user_id": 1})
    return [user["user_id"] for user in users]

# Function to add a new user ID to MongoDB
def add_user_id(user_id):
    if not users_collection.find_one({"user_id": user_id}):
        users_collection.insert_one({"user_id": user_id})

# Function to display progress
async def broadcast_progress(current, total, message, start_time):
    progress = (current / total) * 100
    elapsed_time = time.time() - start_time
    remaining_time = elapsed_time / current * (total - current) if current > 0 else 0
    remaining_time_str = str(int(remaining_time)) + "s" if remaining_time > 0 else "Calculating..."
    
    progress_message = f"Broadcast Progress: {current}/{total} sent\nTime remaining: {remaining_time_str}\n{progress:.2f}%"
    
    # Update the message with progress
    await message.edit(progress_message)

# Command to track new users
@app.on_message(filters.command("start"))
async def start(client, message):
    user_id = message.from_user.id
    add_user_id(user_id)
    await message.reply("Welcome! You will now receive updates.")

# Broadcast command handler
@app.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
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

# Start the bot
print("🎊 I AM ALIVE 🎊  • Support @NT_BOTS_SUPPORT")
app.run()
