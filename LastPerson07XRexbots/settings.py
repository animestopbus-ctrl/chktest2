# LastPerson07XRexbots V2
# Don't Remove Credit
# Telegram Channel @RexBots_Official
# DEVs: 1. @DmOwner 2. @akaza7902

import os
from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from LastPerson07XRexbots.database.db import db
from LastPerson07XRexbots.strings import COMMANDS_TXT

# ======================================================
# /settings - Enhanced Professional Settings Menu V2 (All Functionalities Interconnected)
# ======================================================
@Client.on_message(filters.command("settings") & filters.private)
async def settings_menu(client: Client, message: Message):
    user_id = message.from_user.id
    # Ensure user exists
    if not await db.is_user_exist(user_id):
        await db.add_user(user_id, message.from_user.first_name)

    # Fetch real status
    is_premium = await db.check_premium(user_id)
    premium_badge = "💎 Premium Member" if is_premium else "👤 Free User"

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("📜 Commands List", callback_data="cmd_list_btn")],
        [InlineKeyboardButton("📊 My Usage Stats & Plan", callback_data="user_stats_btn")],
        [InlineKeyboardButton("🗑 Dump Chat", callback_data="dump_chat_btn")],
        [
            InlineKeyboardButton("🖼 Thumbnail", callback_data="thumb_btn"),
            InlineKeyboardButton("📝 Caption", callback_data="caption_btn")
        ],
        [InlineKeyboardButton("🔤 Words Management", callback_data="words_btn")],
        [InlineKeyboardButton("🔑 Session Management", callback_data="session_btn")],
        [InlineKeyboardButton("❌ Close Menu", callback_data="close_btn")]
    ])

    text = (
        f"<b>⚙️ Settings Panel V2</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"<b>Account:</b> {premium_badge}\n"
        f"<b>User ID:</b> <code>{user_id}</code>\n\n"
        f"<i>All features interconnected here. Select to customize.\nDEVs: 1. @DmOwner 2. @akaza7902</i>"
    )

    await message.reply_text(text, reply_markup=buttons, parse_mode=enums.ParseMode.HTML)

# ======================================================
# /commands - Direct Access to Commands List
# ======================================================
@Client.on_message(filters.command("commands") & filters.private)
async def direct_commands(client: Client, message: Message):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("⚙️ Open Settings", callback_data="settings_back_btn"), InlineKeyboardButton("❌ Close", callback_data="close_btn")]
    ])

    await message.reply_text(
        COMMANDS_TXT,
        reply_markup=buttons,
        parse_mode=enums.ParseMode.HTML,
        disable_web_page_preview=True
    )

# ======================================================
# /setchat - Set or Clear Dump Chat (Interconnected)
# ======================================================
@Client.on_message(filters.command("setchat") & filters.private)
async def set_dump_chat(client: Client, message: Message):
    user_id = message.from_user.id
    if not await db.is_user_exist(user_id):
        await db.add_user(user_id, message.from_user.first_name)

    if len(message.command) < 2:
        return await message.reply_text(
            "<b>⚠️ Usage:</b> /setchat <chat_id> or /setchat clear\nDEVs: 1. @DmOwner 2. @akaza7902",
            parse_mode=enums.ParseMode.HTML
        )

    arg = message.command[1].lower()
    if arg == "clear":
        await db.set_dump_chat(user_id, None)
        await message.reply_text("<b>🗑 Dump Chat Cleared!</b>\nDEVs: 1. @DmOwner 2. @akaza7902", parse_mode=enums.ParseMode.HTML)
    else:
        try:
            chat_id = int(arg)
            await db.set_dump_chat(user_id, chat_id)
            await message.reply_text(f"<b>✅ Dump Chat Set to {chat_id}!</b>\nDEVs: 1. @DmOwner 2. @akaza7902", parse_mode=enums.ParseMode.HTML)
        except ValueError:
            await message.reply_text("<b>❌ Invalid Chat ID.</b>\nDEVs: 1. @DmOwner 2. @akaza7902", parse_mode=enums.ParseMode.HTML)

# ======================================================
# CALLBACK QUERY HANDLER FOR SETTINGS (Upgraded Layout)
# ======================================================
@Client.on_callback_query(filters.regex(r"^(cmd_list_btn|user_stats_btn|dump_chat_btn|thumb_btn|caption_btn|words_btn|session_btn|settings_back_btn|close_btn)$"))
async def settings_callback(client: Client, callback_query: CallbackQuery):
    data = callback_query.data
    user_id = callback_query.from_user.id
    message = callback_query.message

    back_close = [
        [InlineKeyboardButton("⬅️ Back to Settings", callback_data="settings_back_btn")],
        [InlineKeyboardButton("❌ Close", callback_data="close_btn")]
    ]

    if data == "cmd_list_btn":
        text = COMMANDS_TXT
        await callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(back_close), parse_mode=enums.ParseMode.HTML)

    elif data == "dump_chat_btn":
        dump_chat = await db.get_dump_chat(user_id)
        status = f"<code>{dump_chat}</code>" if dump_chat else "<b>None Set</b>"
        text = (
            f"<b>🗑 Dump Chat Settings</b>\n\n"
            f"<b>Current:</b> {status}\n\n"
            "<i>Use /setchat <chat_id> to set or /setchat clear to remove.\nDEVs: 1. @DmOwner 2. @akaza7902</i>"
        )
        await callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(back_close), parse_mode=enums.ParseMode.HTML)

    elif data == "thumb_btn":
        thumb_id = await db.get_thumbnail(user_id)
        status = "<b>🟢 Active</b>" if thumb_id else "<b>🔴 Inactive</b>"
        text = (
            f"<b>🖼 Thumbnail Settings</b>\n\n"
            f"<b>Status:</b> {status}\n\n"
            "<i>Commands: /set_thumb, /view_thumb, /del_thumb, /thumb_mode\nDEVs: 1. @DmOwner 2. @akaza7902</i>"
        )
        await callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(back_close), parse_mode=enums.ParseMode.HTML)

    elif data == "caption_btn":
        caption = await db.get_caption(user_id)
        preview = f"<code>{caption}</code>" if caption else "<b>None Set</b>"
        text = (
            f"<b>📝 Caption Settings</b>\n\n"
            f"<b>Current:</b> {preview}\n\n"
            "<i>Commands: /set_caption, /see_caption, /del_caption\nDEVs: 1. @DmOwner 2. @akaza7902</i>"
        )
        await callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(back_close), parse_mode=enums.ParseMode.HTML)

    elif data == "words_btn":
        del_words = await db.get_delete_words(user_id) or []
        repl_words = await db.get_replace_words(user_id) or {}
        del_text = ", ".join(del_words) if del_words else "None"
        repl_text = ", ".join([f"{k} -> {v}" for k,v in repl_words.items()]) if repl_words else "None"
        text = (
            f"<b>🔤 Words Management</b>\n\n"
            f"<b>Delete Words:</b> {del_text}\n"
            f"<b>Replace Words:</b> {repl_text}\n\n"
            "<i>Commands: /set_del_word, /rem_del_word, /set_repl_word, /rem_repl_word\nDEVs: 1. @DmOwner 2. @akaza7902</i>"
        )
        await callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(back_close), parse_mode=enums.ParseMode.HTML)

    elif data == "session_btn":
        session = await db.get_session(user_id)
        status = "<b>✅ Logged In</b>" if session else "<b>❌ Not Logged In</b>"
        text = (
            f"<b>🔑 Session Management</b>\n\n"
            f"<b>Status:</b> {status}\n\n"
            "<i>Commands: /login, /logout\nDEVs: 1. @DmOwner 2. @akaza7902</i>"
        )
        await callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(back_close), parse_mode=enums.ParseMode.HTML)

    elif data == "user_stats_btn":
        # Fetch real stats from DB
        is_premium = await db.check_premium(user_id)
        user_data = await db.col.find_one({'id': int(user_id)})
        
        if is_premium:
            limit_text = "♾️ Unlimited"
            usage_text = "Ignored (Premium)"
        else:
            daily_limit = 10
            used = user_data.get('daily_usage', 0)
            limit_text = f"{daily_limit} Files / 24h"
            usage_text = f"{used} / {daily_limit}"

        text = (
            f"<b>📊 My Usage Statistics V2</b>\n\n"
            f"<b>Plan:</b> {'💎 Premium' if is_premium else '👤 Free'}\n"
            f"<b>Daily Limit:</b> <code>{limit_text}</code>\n"
            f"<b>Today's Usage:</b> <code>{usage_text}</code>\n\n"
            f"<i>Upgrade to Premium for unlimited downloads! /premium\nDEVs: 1. @DmOwner 2. @akaza7902</i>"
        )
        await callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(back_close), parse_mode=enums.ParseMode.HTML)

    elif data == "settings_back_btn":
        # Re-render main menu
        is_premium = await db.check_premium(user_id)
        premium_badge = "💎 Premium Member" if is_premium else "👤 Free User"
        
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("📜 Commands List", callback_data="cmd_list_btn")],
            [InlineKeyboardButton("📊 My Usage Stats & Plan", callback_data="user_stats_btn")],
            [InlineKeyboardButton("🗑 Dump Chat", callback_data="dump_chat_btn")],
            [
                InlineKeyboardButton("🖼 Thumbnail", callback_data="thumb_btn"),
                InlineKeyboardButton("📝 Caption", callback_data="caption_btn")
            ],
            [InlineKeyboardButton("🔤 Words Management", callback_data="words_btn")],
            [InlineKeyboardButton("🔑 Session Management", callback_data="session_btn")],
            [InlineKeyboardButton("❌ Close Menu", callback_data="close_btn")]
        ])
        
        text = (
            f"<b>⚙️ Settings Panel V2</b>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"<b>Account:</b> {premium_badge}\n"
            f"<b>User ID:</b> <code>{user_id}</code>\n\n"
            f"<i>All features interconnected here. Select to customize.\nDEVs: 1. @DmOwner 2. @akaza7902</i>"
        )
        
        await callback_query.edit_message_text(text, reply_markup=buttons, parse_mode=enums.ParseMode.HTML)

    elif data == "close_btn":
        await callback_query.message.delete()

    await callback_query.answer()

# LastPerson07XRexbots V2
# Don't Remove Credit
# Telegram Channel @RexBots_Official
# DEVs: 1. @DmOwner 2. @akaza7902