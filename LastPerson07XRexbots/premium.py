# LastPerson07XRexbots V2
# Don't Remove Credit
# Telegram Channel @RexBots_Official
# DEVs: 1. @DmOwner 2. @akaza7902

from pyrogram import Client, filters, enums
from pyrogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from LastPerson07XRexbots.database.db import db
from config import ADMINS
from datetime import date, datetime, timedelta
from LastPerson07XRexbots.logger import LOGGER

logger = LOGGER(__name__)

# ======================================================
# USER COMMANDS - Professional & Informative
# ======================================================

# /myplan - Detailed Plan & Quota Overview
@Client.on_message(filters.command("myplan") & filters.private)
async def my_plan(client: Client, message: Message):
    user_id = message.from_user.id
    
    # 1. Ensure User Exists (Fixing the 'ensure_user' error manually)
    if not await db.is_user_exist(user_id):
        await db.add_user(user_id, message.from_user.first_name)

    # 2. Fetch User Data Directly from DB
    user_data = await db.col.find_one({'id': user_id})
    
    # Defaults
    is_premium = user_data.get('is_premium', False)
    expiry = user_data.get('premium_expiry')
    daily_usage = user_data.get('daily_usage', 0)
    total_saves = user_data.get('total_saves', 0)  # Assuming tracked

    # 3. Generate Status Text
    if is_premium:
        # Premium Logic
        if expiry:
            try:
                # Handle both date objects and ISO strings
                if isinstance(expiry, (date, datetime)):
                    exp_date = expiry
                else:
                    exp_date = date.fromisoformat(str(expiry))
                
                # Calculate days left
                days_left = (exp_date - date.today()).days if isinstance(exp_date, date) else 999
                expiry_text = f"<code>{expiry}</code> ({days_left} days left)"
            except Exception:
                expiry_text = "<code>Active</code>"
        else:
            expiry_text = "<code>Permanent</code>"

        plan_text = (
            f"<b>👑 Premium Status: Active</b>\n\n"
            f"<b>📅 Expiry:</b> {expiry_text}\n\n"
            f"<b>♾️ Daily Tokens:</b> Unlimited\n"
            f"<b>♾️ Batch Limit:</b> Unlimited\n"
            f"<b>📊 Total Lifetime Saves:</b> <code>{total_saves}</code>\n\n"
            "<i>Thank you for supporting the bot! 🎉\nDEVs: 1. @DmOwner 2. @akaza7902</i>"
        )
    else:
        # Free User Logic (Fixed truncation)
        plan_text = (
            f"<b>👤 Free User Status</b>\n\n"
            f"<b>📅 Expiry:</b> N/A\n\n"
            f"<b>🔢 Daily Tokens:</b> {daily_usage}/10\n"
            f"<b>📦 Batch Limit:</b> 5 files\n"
            f"<b>📊 Total Lifetime Saves:</b> <code>{total_saves}</code>\n\n"
            "<i>Upgrade to premium for unlimited access! /premium\nDEVs: 1. @DmOwner 2. @akaza7902</i>"
        )

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("💎 Upgrade to Premium", callback_data="premium_plans_btn")],
        [InlineKeyboardButton("⚙️ Back to Settings", callback_data="settings_back_btn")]
    ])

    await message.reply_text(plan_text, reply_markup=buttons, parse_mode=enums.ParseMode.HTML)

# /premium - View Premium Plans
@Client.on_message(filters.command("premium") & filters.private)
async def premium_plans(client: Client, message: Message):
    await show_premium_plans(message)

async def show_premium_plans(obj: Message | CallbackQuery):
    text = (
        "<b>💎 Premium Plans V2</b>\n\n"
        "<b>Benefits:</b>\n"
        "• ♾️ Unlimited daily saves\n"
        "• ♾️ Unlimited batch size\n"
        "• Priority support\n"
        "• No ads\n\n"
        "<b>Plans:</b>\n"
        "• 7 Days: $5\n"
        "• 30 Days: $15\n"
        "• Lifetime: $50\n\n"
        "<i>Contact @RexBots_Official to upgrade.\nDEVs: 1. @DmOwner 2. @akaza7902</i>"
    )
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("📞 Contact Support", url="https://t.me/RexBots_Official")],
        [InlineKeyboardButton("⬅️ Back", callback_data="myplan_back_btn")]
    ])
    if isinstance(obj, CallbackQuery):
        await obj.edit_message_text(text, reply_markup=buttons, parse_mode=enums.ParseMode.HTML)
    else:
        await obj.reply_text(text, reply_markup=buttons, parse_mode=enums.ParseMode.HTML)

# ======================================================
# ADMIN COMMANDS - Secure & Logged
# ======================================================

@Client.on_message(filters.command("add_premium") & filters.user(ADMINS) & filters.private)
async def add_premium_admin(client: Client, message: Message):
    if len(message.command) < 3:
        return await message.reply_text(
            "<b>⚠️ Admin Usage:</b>\n"
            "<code>/add_premium &lt;user_id&gt; &lt;days&gt;</code>\n\n"
            "<i>Use 0 for permanent premium.</i>",
            parse_mode=enums.ParseMode.HTML
        )

    try:
        user_id = int(message.command[1])
        days = int(message.command[2])

        if days == 0:
            expiry_date = None
            duration_text = "Permanent"
        else:
            expiry_date = (date.today() + timedelta(days=days)).isoformat()
            duration_text = f"{days} days (until {expiry_date})"

        # Update DB
        await db.add_premium(user_id, expiry_date)

        await message.reply_text(
            f"<b>✅ Premium Added Successfully</b>\n\n"
            f"<b>User ID:</b> <code>{user_id}</code>\n"
            f"<b>Duration:</b> {duration_text}\nDEVs: 1. @DmOwner 2. @akaza7902",
            parse_mode=enums.ParseMode.HTML
        )

    except ValueError:
        await message.reply_text("❌ <b>Error:</b> User ID and Days must be numbers.", parse_mode=enums.ParseMode.HTML)
    except Exception as e:
        await message.reply_text(f"❌ <b>Error:</b> {e}", parse_mode=enums.ParseMode.HTML)

@Client.on_message(filters.command("remove_premium") & filters.user(ADMINS) & filters.private)
async def remove_premium_admin(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(
            "<b>⚠️ Usage:</b> <code>/remove_premium &lt;user_id&gt;</code>",
            parse_mode=enums.ParseMode.HTML
        )
    try:
        user_id = int(message.command[1])
        await db.remove_premium(user_id)
        await message.reply_text(f"✅ Premium removed from <code>{user_id}</code>.\nDEVs: 1. @DmOwner 2. @akaza7902")
    except Exception as e:
        await message.reply_text(f"Error: {e}")

# ======================================================
# CALLBACK QUERIES
# ======================================================

@Client.on_callback_query(filters.regex("^premium_plans_btn$"))
async def premium_plans_callback(client: Client, callback_query: CallbackQuery):
    await show_premium_plans(callback_query)

@Client.on_callback_query(filters.regex("^myplan_back_btn$"))
async def myplan_back_callback(client: Client, callback_query: CallbackQuery):
    # Pass the message object to reuse logic
    await my_plan(client, callback_query.message)

# LastPerson07XRexbots V2
# Don't Remove Credit
# Telegram Channel @RexBots_Official
# DEVs: 1. @DmOwner 2. @akaza7902