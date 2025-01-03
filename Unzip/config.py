import os
import re
from os import environ

id_pattern = re.compile(r'^-?\d+$')

# Define AUTH_CHANNEL at the module level
AUTH_CHANNEL = [
    int(ch) if id_pattern.search(ch) else ch
    for ch in environ.get('AUTH_CHANNEL', '-1001764441595 -1002135593873').split()
]

# Define MONGO_URL at the module level
MONGO_URL = os.environ.get("MONGO_URL", "")  # Fetch MongoDB URL from environment variables

class config(object):
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    API_ID = int(os.environ.get("API_ID", "0"))
    API_HASH = os.environ.get("API_HASH", "")
