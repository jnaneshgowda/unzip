# ©️ LISA-KOREA | @LISA_FAN_LK | NT_BOT_CHANNEL | LISA-KOREA/UnZip-Bot

# [⚠️ Do not change this repo link ⚠️] :- https://github.com/LISA-KOREA/UnZip-Bot

from pyrogram import Client, filters
from Unzip.config import config

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

# Function to get all user IDs (replace with actual logic to retrieve user IDs)
def get_all_user_ids():
    # This function should return a list of user IDs who have interacted with the bot
    # For now, it returns an empty list, but you should implement it to fetch actual user IDs
    return [123456789, 987654321]  # Example user IDs

# Broadcast command handler
@app.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast(client, message):
    if len(message.command) < 2:
        await message.reply("Please provide a message to broadcast.")
        return

    broadcast_message = message.text.split(None, 1)[1]
    
    # Get the list of user IDs to send the broadcast message to
    user_ids = get_all_user_ids()

    # Send the broadcast message to all users
    for user_id in user_ids:
        try:
            await client.send_message(user_id, broadcast_message)
        except Exception as e:
            print(f"Failed to send message to {user_id}: {e}")

    await message.reply("Broadcast completed.")

# Start the bot
print("🎊 I AM ALIVE 🎊  • Support @NT_BOTS_SUPPORT")
app.run()
