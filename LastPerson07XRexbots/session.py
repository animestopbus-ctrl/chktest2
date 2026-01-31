# LastPerson07XRexbots V2
# Don't Remove Credit
# Telegram Channel @RexBots_Official
# DEVs: 1. @DmOwner 2. @akaza7902

import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)
from pyrogram import enums
from config import API_ID, API_HASH
from LastPerson07XRexbots.database.db import db

# ==========================================
# STATE MANAGEMENT (Optimized for traffic)
# ==========================================
LOGIN_STATE = {}
cancel_keyboard = ReplyKeyboardMarkup(
    [[KeyboardButton("❌ Cancel")]],
    resize_keyboard=True
)
remove_keyboard = ReplyKeyboardRemove()

# Progress indicators
PROGRESS_STEPS = {
    "WAITING_PHONE": "🟢 Phone Number → 🔵 Code → 🔵 Password",
    "WAITING_CODE": "✅ Phone Number → 🟢 Code → 🔵 Password",
    "WAITING_PASSWORD": "✅ Phone Number → ✅ Code → 🟢 Password"
}

# Emoji-based loading animation
LOADING_FRAMES = [
    "🔄 Connecting •••",
    "🔄 Connecting ••○",
    "🔄 Connecting •○○",
    "🔄 Connecting ○○○",
    "🔄 Connecting ○○•",
    "🔄 Connecting ○••",
    "🔄 Connecting •••"
]

async def animate_loading(message: Message, duration: int = 5):
    for _ in range(duration):
        for frame in LOADING_FRAMES:
            try:
                await message.edit_text(f"<b>{frame}</b>", parse_mode=enums.ParseMode.HTML)
                await asyncio.sleep(0.5)
            except:
                return

# ---------------------------------------------------
# /login - Start Login Process (Interconnected with settings)
# ---------------------------------------------------
@Client.on_message(filters.private & filters.command("login"))
async def login_start(client: Client, message: Message):
    user_id = message.from_user.id
   
    # Check if already logged in
    user_data = await db.get_session(user_id)
    if user_data:
        return await message.reply(
            "<b>✅ You're already logged in! 🎉</b>\n\n"
            "To switch accounts, first use /logout.\nDEVs: 1. @DmOwner 2. @akaza7902",
            parse_mode=enums.ParseMode.HTML
        )
    # Initialize State
    LOGIN_STATE[user_id] = {"step": "WAITING_PHONE", "data": {}}
   
    progress = PROGRESS_STEPS["WAITING_PHONE"]
    await message.reply(
        f"<b>👋 Hey! Let's log you in smoothly 🌟</b>\n\n"
        f"<i>Progress: {progress}</i>\n\n"
        "📞 Please send your <b>Telegram Phone Number</b> with country code.\n\n"
        "<i>Example: +1234567890\nDEVs: 1. @DmOwner 2. @akaza7902</i>",
        reply_markup=cancel_keyboard,
        parse_mode=enums.ParseMode.HTML
    )

# ---------------------------------------------------
# /logout - Logout Process
# ---------------------------------------------------
@Client.on_message(filters.private & filters.command("logout"))
async def logout(client: Client, message: Message):
    user_id = message.from_user.id
    session = await db.get_session(user_id)
    if not session:
        return await message.reply("<b>❌ You're not logged in.</b>\nDEVs: 1. @DmOwner 2. @akaza7902", parse_mode=enums.ParseMode.HTML)
    
    await db.del_session(user_id)
    await message.reply("<b>✅ Successfully logged out! 🔓</b>\n\n<i>Use /login to log in again.\nDEVs: 1. @DmOwner 2. @akaza7902</i>", parse_mode=enums.ParseMode.HTML)

# ---------------------------------------------------
# HANDLE LOGIN STATES (Text Messages During Login)
# ---------------------------------------------------
@Client.on_message(filters.private & filters.text & ~filters.command, group=1)
async def login_handler(client: Client, message: Message):
    user_id = message.from_user.id
    text = message.text.strip()
    
    if user_id not in LOGIN_STATE:
        return  # Not in login state
    
    state = LOGIN_STATE[user_id]
    step = state["step"]
    progress = PROGRESS_STEPS[step]
    
    # Cancel Option
    if text.lower() == "❌ cancel":
        del LOGIN_STATE[user_id]
        await message.reply("<b>❌ Login Cancelled.</b>\n\n<i>Use /login to start again.\nDEVs: 1. @DmOwner 2. @akaza7902</i>", reply_markup=remove_keyboard, parse_mode=enums.ParseMode.HTML)
        return
    
    # STEP 1: WAITING FOR PHONE
    if step == "WAITING_PHONE":
        phone_number = text
        status_msg = await message.reply(
            f"<b>📱 Verifying phone... 📱</b>\n\n<i>Progress: {progress}</i>",
            parse_mode=enums.ParseMode.HTML
        )
        # Short animation
        animation_task = asyncio.create_task(animate_loading(status_msg, duration=3))
        
        try:
            temp_client = Client(
                f"temp_{user_id}",
                api_id=API_ID,
                api_hash=API_HASH,
                in_memory=True
            )
            await temp_client.connect()
            sent_code = await temp_client.send_code(phone_number)
            animation_task.cancel()
            
            # Update State
            state["step"] = "WAITING_CODE"
            state["data"] = {
                "client": temp_client,
                "phone_number": phone_number,
                "phone_code_hash": sent_code.phone_code_hash
            }
            
            await status_msg.edit(
                "<b>✅ Phone Verified! ✅</b>\n\n"
                f"<i>Progress: {PROGRESS_STEPS['WAITING_CODE']}</i>\n\n"
                "🔢 Please send the <b>OTP Code</b> you received.\n\n"
                "<i>Example: If code is 12345, send 12345\nDEVs: 1. @DmOwner 2. @akaza7902</i>",
                parse_mode=enums.ParseMode.HTML
            )
        except ApiIdInvalid:
            animation_task.cancel()
            await status_msg.edit("<b>❌ Invalid API ID/Hash. Contact support.</b>\nDEVs: 1. @DmOwner 2. @akaza7902", parse_mode=enums.ParseMode.HTML)
            del LOGIN_STATE[user_id]
        except PhoneNumberInvalid:
            animation_task.cancel()
            await status_msg.edit("<b>❌ Invalid Phone Number. Try again.</b>\nDEVs: 1. @DmOwner 2. @akaza7902", parse_mode=enums.ParseMode.HTML)
        except Exception as e:
            animation_task.cancel()
            await status_msg.edit(f"<b>❌ Error: {e}</b>\nDEVs: 1. @DmOwner 2. @akaza7902", parse_mode=enums.ParseMode.HTML)
            del LOGIN_STATE[user_id]
    
    # STEP 2: WAITING FOR CODE
    elif step == "WAITING_CODE":
        code = text
        temp_client = state["data"]["client"]
        phone_number = state["data"]["phone_number"]
        phone_code_hash = state["data"]["phone_code_hash"]
        
        status_msg = await message.reply(
            f"<b>🔢 Verifying code... 🔢</b>\n\n<i>Progress: {progress}</i>",
            parse_mode=enums.ParseMode.HTML
        )
        # Short animation
        animation_task = asyncio.create_task(animate_loading(status_msg, duration=3))
        
        try:
            await temp_client.sign_in(phone_number, phone_code_hash, code)
            animation_task.cancel()
            await finalize_login(status_msg, temp_client, user_id)
        except PhoneCodeInvalid:
            animation_task.cancel()
            await status_msg.edit("<b>❌ Invalid Code. Try again.</b>\nDEVs: 1. @DmOwner 2. @akaza7902", parse_mode=enums.ParseMode.HTML)
        except PhoneCodeExpired:
            animation_task.cancel()
            await status_msg.edit("<b>❌ Code Expired. Restart /login.</b>\nDEVs: 1. @DmOwner 2. @akaza7902", parse_mode=enums.ParseMode.HTML)
            del LOGIN_STATE[user_id]
        except SessionPasswordNeeded:
            animation_task.cancel()
            state["step"] = "WAITING_PASSWORD"
            await status_msg.edit(
                "<b>🔒 2FA Detected! 🔒</b>\n\n"
                f"<i>Progress: {PROGRESS_STEPS['WAITING_PASSWORD']}</i>\n\n"
                "🔑 Please send your <b>2FA Password</b>.\nDEVs: 1. @DmOwner 2. @akaza7902",
                parse_mode=enums.ParseMode.HTML
            )
        except Exception as e:
            animation_task.cancel()
            await status_msg.edit(f"<b>❌ Error: {e}</b>\nDEVs: 1. @DmOwner 2. @akaza7902", parse_mode=enums.ParseMode.HTML)
            await temp_client.disconnect()
            del LOGIN_STATE[user_id]
    
    # STEP 3: WAITING FOR PASSWORD (2FA)
    elif step == "WAITING_PASSWORD":
        password = text
        temp_client = state["data"]["client"]
       
        status_msg = await message.reply(
            f"<b>🔑 Checking password... 🔑</b>\n\n<i>Progress: {progress}</i>",
            parse_mode=enums.ParseMode.HTML
        )
        # Short animation
        animation_task = asyncio.create_task(animate_loading(status_msg, duration=3))
       
        try:
            await temp_client.check_password(password=password)
            animation_task.cancel()
            await finalize_login(status_msg, temp_client, user_id)
        except PasswordHashInvalid:
            animation_task.cancel()
            await status_msg.edit(
                "<b>❌ Incorrect password. 🔑</b>\n\n"
                f"<i>Progress: {progress}</i>\n\nPlease try again.\nDEVs: 1. @DmOwner 2. @akaza7902",
                parse_mode=enums.ParseMode.HTML
            )
        except Exception as e:
            animation_task.cancel()
            await status_msg.edit(
                f"<b>❌ Something went wrong: {e} 🤔</b>\n\n<i>Progress: {progress}</i>\nDEVs: 1. @DmOwner 2. @akaza7902",
                parse_mode=enums.ParseMode.HTML
            )
            await temp_client.disconnect()
            del LOGIN_STATE[user_id]

# ---------------------------------------------------
# FINALIZE LOGIN (Save Session)
# ---------------------------------------------------
async def finalize_login(status_msg: Message, temp_client, user_id):
    try:
        # Generate String Session
        session_string = await temp_client.export_session_string()
        await temp_client.disconnect()
       
        # Save to DB
        await db.set_session(user_id, session=session_string)
       
        # Clear State
        if user_id in LOGIN_STATE:
            del LOGIN_STATE[user_id]
           
        # Success message
        await status_msg.edit(
            "<b>🎉 Login Successful! 🌟</b>\n\n"
            "<i>Progress: ✅ Phone Number → ✅ Code → ✅ Password</i>\n\n"
            "<i>Your session has been saved securely. 🔒</i>\n\n"
            "You can now use all features! 🚀\nDEVs: 1. @DmOwner 2. @akaza7902",
            parse_mode=enums.ParseMode.HTML,
            reply_markup=remove_keyboard
        )
    except Exception as e:
        await status_msg.edit(
            f"<b>❌ Failed to save session: {e} 😔</b>\n\nPlease try /login again.\nDEVs: 1. @DmOwner 2. @akaza7902",
            parse_mode=enums.ParseMode.HTML,
            reply_markup=remove_keyboard
        )
        if user_id in LOGIN_STATE:
            del LOGIN_STATE[user_id]

# LastPerson07XRexbots V2
# Don't Remove Credit
# Telegram Channel @RexBots_Official
# DEVs: 1. @DmOwner 2. @akaza7902