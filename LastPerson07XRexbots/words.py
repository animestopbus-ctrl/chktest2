# LastPerson07XRexbots V2
# Don't Remove Credit
# Telegram Channel @RexBots_Official
# DEVs: 1. @DmOwner 2. @akaza7902

from pyrogram import Client, filters
from pyrogram.types import Message
from LastPerson07XRexbots.database.db import db

@Client.on_message(filters.command("set_del_word") & filters.private)
async def set_del_word(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("**Usage:** `/set_del_word word1 word2 ...`\n\nThese words will be automatically removed from captions and filenames.\nDEVs: 1. @DmOwner 2. @akaza7902")
    
    words = message.command[1:]
    await db.set_delete_words(message.from_user.id, words)
    await message.reply_text(f"**Added {len(words)} words to delete list.**\nDEVs: 1. @DmOwner 2. @akaza7902")

@Client.on_message(filters.command("rem_del_word") & filters.private)
async def rem_del_word(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("**Usage:** `/rem_del_word word1 word2 ...`\nDEVs: 1. @DmOwner 2. @akaza7902")
    
    words = message.command[1:]
    await db.remove_delete_words(message.from_user.id, words)
    await message.reply_text(f"**Removed {len(words)} words from delete list.**\nDEVs: 1. @DmOwner 2. @akaza7902")

# LastPerson07XRexbots V2
# Don't Remove Credit
# Telegram Channel @RexBots_Official
# DEVs: 1. @DmOwner 2. @akaza7902

@Client.on_message(filters.command("set_repl_word") & filters.private)
async def set_repl_word(client: Client, message: Message):
    # Syntax: /set_repl_word target replacement
    if len(message.command) < 3:
        return await message.reply_text("**Usage:** `/set_repl_word target replacement`\n\nExample: `/set_repl_word @OldChannel @NewChannel`\nDEVs: 1. @DmOwner 2. @akaza7902")
    
    target = message.command[1]
    replacement = message.command[2]
    
    await db.set_replace_words(message.from_user.id, {target: replacement})
    await message.reply_text(f"**Set replacement:** `{target}` -> `{replacement}`\nDEVs: 1. @DmOwner 2. @akaza7902")

@Client.on_message(filters.command("rem_repl_word") & filters.private)
async def rem_repl_word(client: Client, message: Message):
    if len(message.command) < 2:
         return await message.reply_text("**Usage:** `/rem_repl_word target`\nDEVs: 1. @DmOwner 2. @akaza7902")
    
    target = message.command[1]
    await db.remove_replace_words(message.from_user.id, [target])
    await message.reply_text(f"**Removed replacement for:** `{target}`\nDEVs: 1. @DmOwner 2. @akaza7902")

# LastPerson07XRexbots V2
# Don't Remove Credit
# Telegram Channel @RexBots_Official
# DEVs: 1. @DmOwner 2. @akaza7902