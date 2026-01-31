# LastPerson07XRexbots V2
# Don't Remove Credit
# Telegram Channel @RexBots_Official
# DEVs: 1. @DmOwner 2. @akaza7902

import asyncio
from asyncio import Semaphore  # Fixed import for rate limiting high traffic
import datetime
import sys
import os
from datetime import timezone, timedelta

from pyrogram import Client, filters, enums, __version__ as pyrogram_version
from pyrogram.types import Message

from config import API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL
from LastPerson07XRexbots.database.db import db
from LastPerson07XRexbots.logger import LOGGER

# ✅ Keep-alive server (For Render / Heroku)
try:
    from LastPerson07XRexbots.keep_alive import keep_alive
except ImportError:
    keep_alive = None

logger = LOGGER(__name__)

# ✅ Indian Standard Time
IST = timezone(timedelta(hours=5, minutes=30))

# ==============================================================================
# 🎨 CUSTOM BANNER (Printed in Terminal)
# ==============================================================================
LOGO = r"""


  ██████╗  ██╗  ██╗  █████╗  ███╗   ██╗ ██████╗   █████╗  ██╗      
  ██╔══██╗ ██║  ██║ ██╔══██╗ ████╗  ██║ ██╔══██╗ ██╔══██╗ ██║      
  ██║  ██║ ███████║ ███████║ ██╔██╗ ██║ ██████╔╝ ███████║ ██║      
  ██║  ██║ ██╔══██║ ██╔══██║ ██║╚██╗██║ ██╔═══╝  ██╔══██║ ██║      
  ██████╔╝ ██║  ██║ ██║  ██║ ██║ ╚████║ ██║      ██║  ██║ ███████



    𝙱𝙾𝚃 𝚆𝙾𝚁𝙺𝙸𝙽𝙶 𝙿𝚁𝙾𝙿𝙴𝚁𝙻𝚈.... V2 (High Traffic Ready)
    DEVs: 1. @DmOwner 2. @akaza7902
"""

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="LastPerson07XRexbots_Login_Bot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="LastPerson07XRexbots"), 
            
            # ==================================================================
            # 🚀 SPEED & PERFORMANCE UPGRADES (For High Traffic)
            # ==================================================================
            workers=50,                         # Increased for heavy load
            sleep_threshold=15,                 # Auto-sleep on FloodWait
            max_concurrent_transmissions=20,    # ⚡ Upload Speed Boost (20x)
            ipv6=False,                         # Disable IPv6 for stability
            in_memory=False,                    # Keep session on disk
            # ==================================================================
        )
        self.rate_limiter = Semaphore(10)  # Limit to 10 concurrent ops for flood prevention

    async def start(self):
        # 🔹 Print Banner to Terminal
        print(LOGO)
        
        await super().start()
        me = await self.get_me()

        # 🔹 Log Start to Channel (Rate limited)
        async with self.rate_limiter:
            now = datetime.datetime.now(IST)
            start_text = (
                f"<b><i>✅ Bot @{me.username} Started</i></b>\n\n"
                f"<b>📅 Date:</b> <code>{now.strftime('%d %B %Y')}</code>\n"
                f"<b>🕒 Time:</b> <code>{now.strftime('%I:%M %p')} IST</code>\n\n"
                f"<b>Developed by DEVs: 1. @DmOwner 2. @akaza7902</b>"
            )
            try:
                await self.send_message(
                    LOG_CHANNEL,
                    start_text,
                    parse_mode=enums.ParseMode.HTML
                )
            except Exception as e:
                logger.error(f"Failed to send start log: {e}")

        logger.info(f"Bot @{me.username} started successfully (V2)")

        if keep_alive:
            keep_alive()

    async def stop(self):
        me = await self.get_me()
        now = datetime.datetime.now(IST)

        stop_text = (
            f"<b><i>❌ Bot @{me.username} Stopped</i></b>\n\n"
            f"<b>📅 Date:</b> <code>{now.strftime('%d %B %Y')}</code>\n"
            f"<b>🕒 Time:</b> <code>{now.strftime('%I:%M %p')} IST</code>\n\n"
            f"<b>Developed by DEVs: 1. @DmOwner 2. @akaza7902</b>"
        )

        try:
            await self.send_message(
                LOG_CHANNEL,
                stop_text,
                parse_mode=enums.ParseMode.HTML
            )
        except Exception as e:
            logger.error(f"Failed to send stop log: {e}")

        await super().stop()
        logger.info("Bot stopped cleanly")

BotInstance = Bot()

# ========================================================
# ✅ NEW USER LOGGER (Rate limited for high traffic)
# Logs only on FIRST interaction
# ========================================================
@BotInstance.on_message(filters.private & filters.incoming, group=-1)
async def new_user_log(bot: Client, message: Message):
    async with bot.rate_limiter:  # Rate limit logs
        user = message.from_user
        if not user:
            return

        # 1. Check if user exists (Cached)
        if await db.is_user_exist(user.id):
            return

        # 2. Add user if not exists
        await db.add_user(user.id, user.first_name)

        # 3. Log the new user
        now = datetime.datetime.now(IST)
        username_text = f"@{user.username}" if user.username else "<i>None</i>"

        new_user_text = (
            f"<b><i>#NewUser 👤 Joined the Bot</i></b>\n\n"
            f"<b>Bot:</b> @{bot.me.username}\n\n"
            f"<b>User:</b> {user.mention(style='html')}\n"
            f"<b>Username:</b> {username_text}\n"
            f"<b>User ID:</b> <code>{user.id}</code>\n\n"
            f"<b>📅 Date:</b> <code>{now.strftime('%d %B %Y')}</code>\n"
            f"<b>🕒 Time:</b> <code>{now.strftime('%I:%M %p')} IST</code>\n\n"
            f"<b>Developed by DEVs: 1. @DmOwner 2. @akaza7902</b>"
        )

        try:
            await bot.send_message(
                LOG_CHANNEL,
                new_user_text,
                parse_mode=enums.ParseMode.HTML,
                disable_web_page_preview=True
            )
            logger.info(f"New user logged: {user.id} - {user.first_name}")
        except Exception as e:
            logger.error(f"Failed to log new user {user.id}: {e}")

if __name__ == "__main__":
    BotInstance.run()

# LastPerson07XRexbots V2
# Don't Remove Credit
# Telegram Channel @RexBots_Official
# DEVs: 1. @DmOwner 2. @akaza7902
