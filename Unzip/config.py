import os

class Config(object):
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    API_ID = int(os.environ.get("API_ID", ""))
    API_HASH = os.environ.get("API_HASH", "")

    # Force Subscription Channel IDs
    FORCE_SUB_CHANNELS = [
        -1001764441595,  # Replace with your first channel ID
        -1002135593873,  # Replace with your second channel ID
    ]
