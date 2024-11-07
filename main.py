import os
import logging
import asyncio
from pyrogram import Client as AFK, idle
from pyrogram import enums
from pyromod import listen
from tglogging import TelegramLogHandler

# Config
class Config(object):
    BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
    API_ID = int(os.getenv("API_ID", "YOUR_API_ID_HERE"))
    API_HASH = os.getenv("API_HASH", "YOUR_API_HASH_HERE")
    DOWNLOAD_LOCATION = "./DOWNLOADS"
    SESSIONS = "./SESSIONS"

    AUTH_USERS = os.getenv('AUTH_USERS', '902551614').split(',')
    AUTH_USERS = [int(user) for user in AUTH_USERS]

    GROUPS = os.getenv('GROUPS', '-1002340898616').split(',')
    GROUPS = [int(group) for group in GROUPS]

    LOG_CH = os.getenv("LOG_CH", "-1002202175238")


# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        TelegramLogHandler(
            token=Config.BOT_TOKEN,
            log_chat_id=Config.LOG_CH,
            update_interval=2,
            minimum_lines=1,
            pending_logs=200000
        ),
        logging.StreamHandler()
    ]
)

LOGGER = logging.getLogger(__name__)
LOGGER.info("Live log streaming to Telegram.")

# Directory Setup
if not os.path.isdir(Config.DOWNLOAD_LOCATION):
    os.makedirs(Config.DOWNLOAD_LOCATION)
if not os.path.isdir(Config.SESSIONS):
    os.makedirs(Config.SESSIONS)

# Client Setup
plugins = dict(root="plugins")

PRO = AFK(
    "AFK-DL",
    bot_token=Config.BOT_TOKEN,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    sleep_threshold=120,
    plugins=plugins,
    workdir=f"{Config.SESSIONS}/",
    workers=2
)

# Chat IDs: Add both GROUPS and AUTH_USERS to chat_id list
chat_id = Config.GROUPS + Config.AUTH_USERS

async def main():
    await PRO.start()
    
    bot_info = await PRO.get_me()
    LOGGER.info(f"<--- @{bot_info.username} Started --->")
    
    # Send messages to specified chat IDs
    for i in chat_id:
        try:
            await PRO.send_message(chat_id=i, text="**Bot Started! ♾ /pro **")
        except Exception as e:
            LOGGER.error(f"Failed to send message to {i}: {e}")
            continue
    
    await idle()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
    LOGGER.info("<--- Bot Stopped --->")
