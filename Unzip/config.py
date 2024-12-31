import os
from os import environ

id_pattern = re.compile(r'^.\d+$')

class config(object):
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    API_ID = int(os.environ.get("API_ID", ""))
    API_HASH = os.environ.get("API_HASH", "")
    AUTH_CHANNEL = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('AUTH_CHANNEL', '-1001764441595 -1002135593873').split()] # give channel id with seperate space. Ex : ('-10073828 -102782829 -1007282828')
    
