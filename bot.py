import time
from pymongo import MongoClient
from pyrogram import Client
from Unzip.config import MONGO_URL, config
import asyncio

# MongoDB connection setup
client = MongoClient(MONGO_URL)  # Use MongoDB URL from the config
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

# Start the bot
print("🎊 I AM ALIVE 🎊  • Support @JN2FLIX")
app.run()
