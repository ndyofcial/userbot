import os
from PIL import Image, ImageDraw, ImageFont, ImageOps
from pyrogram import Client
from pyrogram.types import Message, User, Chat
from PyroUbot import *
from io import BytesIO

from pyrogram.types import Chat

__MODULE__ = "ᴄᴇᴋ ɪᴅ"
__HELP__ = """
<b>⦪ ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴄᴇᴋ ɪᴅ ⦫</b>
<blockquote>⎆ perintah :
ᚗ <code>{0}cekid</code>
⊶ Untuk Mengambil Data User/Channel/Grup.
</blockquote>
<blockquote>⎆ perintah :
ᚗ <code>{0}id</code>
⊶ Untuk Mengambil Data User
</blockquote>
"""

async def cekid_handler(client, message):
    user = message.from_user
    chat = message.chat

    # ========== Private Chat (user ↔ user) ==========
    if chat.type == "private":
        if message.reply_to_message and message.reply_to_message.from_user:
            replied = message.reply_to_message
            replied_user = replied.from_user
            text = f"""Message ID: <code>{message.id}</code>
Your ID: <code>{user.id}</code>
Chat ID: <code>{chat.id}</code>

Replied Message Information:
├ Message ID: <code>{replied.id}</code>
├ User ID: <code>{replied_user.id}</code>"""
        else:
            text = f"""Message ID: <code>{message.id}</code>
Your ID: <code>{user.id}</code>
Chat ID: <code>{chat.id}</code>"""

    # ========== Bot Chat (user ↔ bot) ==========
    elif chat.type == "bot":
        text = f"""Message ID: <code>{message.id}</code>
Your ID: <code>{user.id}</code>
Bot Chat ID: <code>{chat.id}</code>"""

    # ========== Group / Supergroup ==========
    elif chat.type in ["group", "supergroup"]:
        chat_title = chat.title or "Group"
        username_text = f"@{user.username}" if user.username else "Tidak ada"
        digit_info = f"({len(str(user.id))} digit)"
        text = f"""✉️ Msg ID: <code>{message.id}</code>
👤 Nama: {user.first_name}
🔗 Username: {username_text}
🆔 User ID: <code>{user.id}</code> {digit_info}
💬 Chat ID: <code>{chat.id}</code> ({chat_title})"""

        if message.reply_to_message and message.reply_to_message.from_user:
            replied = message.reply_to_message
            replied_user = replied.from_user
            text += f"""

Replied Message Information:
├ Message ID: <code>{replied.id}</code>
├ User ID: <code>{replied_user.id}</code>"""

    # ========== Channel ==========
    elif chat.type == "channel":
        chat_title = chat.title or "Channel"
        text = f"""✉️ Msg ID: <code>{message.id}</code>
💬 Chat ID: <code>{chat.id}</code> ({chat_title})"""

    else:
        text = f"Chat type tidak dikenal: {chat.type}"

    await message.reply(text, quote=True)


# UBOT
@PY.UBOT("id|cekid|myid")
async def _(client, message):
    await cekid_handler(client, message)

# BOT
@PY.BOT("id|cekid|myid")
async def _(client, message):
    await cekid_handler(client, message)
