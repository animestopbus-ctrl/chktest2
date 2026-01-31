# LastPerson07XRexbots V2
# Don't Remove Credit
# Telegram Channel @RexBots_Official
# DEVs: 1. @DmOwner 2. @akaza7902

import os
import asyncio
import random
import time
import shutil
import aiohttp  # Added for API fetches
import pyrogram
from pyrogram import Client, filters, enums
from pyrogram.errors import (
    FloodWait, UserIsBlocked, InputUserDeactivated, UserAlreadyParticipant, 
    InviteHashExpired, UsernameNotOccupied, AuthKeyUnregistered, UserDeactivated, UserDeactivatedBan
)
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery, InputMediaPhoto
from config import API_ID, API_HASH, ERROR_MESSAGE
from LastPerson07XRexbots.database.db import db
import math
from LastPerson07XRexbots.logger import LOGGER
from LastPerson07XRexbots.strings import ABOUT_TXT, HELP_TXT  # Imported from strings.py

# ==============================================================================
# ⚙️ SYSTEM CONFIGURATION & ASSETS
# ==============================================================================

logger = LOGGER(__name__)

# --- Dynamic Wallpapers via API (Picsum.photos - random high-res wallpapers) ---
async def get_random_wallpaper():
    async with aiohttp.ClientSession() as session:
        try:
            seed = random.randint(1, 1000000)  # Random seed for variety
            url = f"https://picsum.photos/seed/{seed}/1200/800"
            async with session.get(url) as resp:
                if resp.status == 200:
                    return url  # Direct URL for InputMediaPhoto
        except Exception as e:
            logger.error(f"Wallpaper API error: {e}")
    return "https://picsum.photos/1200/800"  # Fallback default

# --- Static Assets ---
SUBSCRIPTION = os.environ.get('SUBSCRIPTION', 'https://graph.org/file/242b7f1b52743938d81f1.jpg')

# --- Operational Limits ---
FREE_LIMIT_SIZE = 2 * 1024 * 1024 * 1024  # 2 GB Limit for Free Users
FREE_LIMIT_DAILY = 10                     # 10 Files per 24h

# --- Payment Info ---
UPI_ID = os.environ.get("UPI_ID", "your_upi@oksbi")
QR_CODE = os.environ.get("QR_CODE", "https://graph.org/file/your_qr_code.jpg")

# --- Engagement ---
REACTIONS = [
    "👍", "❤️", "🔥", "🥰", "👏", "😁", "🤔", "🤯", "😱", "🤬", 
    "😢", "🎉", "🤩", "🤮", "💩", "🙏", "👌", "🕊", "🤡", "🥱", 
    "🥴", "😍", "🐳", "❤️‍🔥", "🌚", "🌭", "💯", "🤣", "⚡", "🍌", 
    "🏆", "💔", "🤨", "😐", "🍓", "🍾", "💋", "🖕", "😈", "😴", 
    "😭", "🤓", "👻", "👨‍💻", "👀", "🎃", "🙈", "😇", "😨", "🤝", 
    "✍", "🤗", "🫡", "🎅", "🎄", "☃", "💅"
]

START_TXT = """<b>👋 Hello {mention}!</b>

I'm {bot_first_name}, your advanced save restricted content bot V2. Send me a link to save media/files.

<b>Quota:</b> {quota_info}

DEVs: 1. @DmOwner 2. @akaza7902
Community: @RexBots_Official (Do not alter or bot will break)"""

# ==============================================================================
# /start COMMAND - Upgraded UI with Dynamic Wallpaper
# ==============================================================================
@Client.on_message(filters.command("start") & filters.private)
async def start_command(client: Client, message: Message):
    user_id = message.from_user.id
    if not await db.is_user_exist(user_id):
        await db.add_user(user_id, message.from_user.first_name)

    bot = await client.get_me()
    wallpaper_url = await get_random_wallpaper()

    # Get quota info (interconnected with premium)
    user_data = await db.col.find_one({'id': user_id})
    is_premium = user_data.get('is_premium', False)
    daily_usage = user_data.get('daily_usage', 0)
    quota_info = "Unlimited (Premium)" if is_premium else f"{daily_usage}/10 saves today"

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("💎 Buy Premium", callback_data="buy_premium"),
            InlineKeyboardButton("🆘 Help & Guide", callback_data="help_btn")
        ],
        [
            InlineKeyboardButton("⚙️ Settings Panel", callback_data="settings_btn"),
            InlineKeyboardButton("ℹ️ About Bot", callback_data="about_btn")
        ],
        [InlineKeyboardButton('👨‍💻 DEVs: 1. @DmOwner 2. @akaza7902', url='https://t.me/RexBots_Official')]
    ])

    await message.reply_photo(
        photo=wallpaper_url,
        caption=START_TXT.format(
            mention=message.from_user.mention,
            bot_username=bot.username,
            bot_first_name=bot.first_name,
            quota_info=quota_info
        ),
        reply_markup=buttons,
        parse_mode=enums.ParseMode.HTML
    )

# ==============================================================================
# CALLBACK QUERY HANDLER - Upgraded with Interconnectivity
# ==============================================================================
@Client.on_callback_query()
async def callback_handler(client: Client, callback_query: CallbackQuery):
    data = callback_query.data
    message = callback_query.message

    # --- PREMIUM MENU ---
    if data == "buy_premium":
        buttons = [[InlineKeyboardButton("⬅️ Back to Home", callback_data="start_btn")]]
        await client.edit_message_media(
            chat_id=message.chat.id,
            message_id=message.id,
            media=InputMediaPhoto(
                media=SUBSCRIPTION, 
                caption="<b>💎 Premium Subscription</b>\n\nContact for details.\nDEVs: 1. @DmOwner 2. @akaza7902"
            ),
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    # --- HELP MENU ---
    elif data == "help_btn":
        buttons = [[InlineKeyboardButton("⬅️ Back to Home", callback_data="start_btn")]]
        await client.edit_message_caption(
            chat_id=message.chat.id,
            message_id=message.id,
            caption=HELP_TXT,
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=enums.ParseMode.HTML
        )
    
    # --- ABOUT MENU ---
    elif data == "about_btn":
        buttons = [[InlineKeyboardButton("⬅️ Back to Home", callback_data="start_btn")]]
        await client.edit_message_caption(
            chat_id=message.chat.id,
            message_id=message.id,
            caption=ABOUT_TXT,
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=enums.ParseMode.HTML
        )

    # --- HOME / START MENU ---
    elif data == "start_btn":
        bot = await client.get_me()
        wallpaper_url = await get_random_wallpaper()
        buttons = [
            [
                InlineKeyboardButton("💎 Buy Premium", callback_data="buy_premium"),
                InlineKeyboardButton("🆘 Help & Guide", callback_data="help_btn")
            ],
            [
                InlineKeyboardButton("⚙️ Settings Panel", callback_data="settings_btn"),
                InlineKeyboardButton("ℹ️ About Bot", callback_data="about_btn")
            ],
            [InlineKeyboardButton('👨‍💻 DEVs: 1. @DmOwner 2. @akaza7902', url='https://t.me/RexBots_Official')]
        ]
        # Rotate Image via API
        await client.edit_message_media(
            chat_id=message.chat.id,
            message_id=message.id,
            media=InputMediaPhoto(
                media=wallpaper_url,
                caption=START_TXT.format(callback_query.from_user.mention, bot.username, bot.first_name)
            ),
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    # --- CLOSE BUTTON ---
    elif data == "close_btn":
        await message.delete()

    # --- SETTINGS SUB-MENUS (Handled by settings.py) ---
    elif data in ["cmd_list_btn", "user_stats_btn", "dump_chat_btn", "thumb_btn", "caption_btn", "words_btn", "session_btn"]:
        pass

    await callback_query.answer()

# LastPerson07XRexbots V2
# Don't Remove Credit
# Telegram Channel @RexBots_Official
# DEVs: 1. @DmOwner 2. @akaza7902