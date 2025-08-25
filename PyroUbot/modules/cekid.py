import os
from PIL import Image, ImageDraw, ImageFont, ImageOps
from pyrogram import Client
from pyrogram.types import Message, User, Chat
from PyroUbot import *
from io import BytesIO

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

    # ========== Private Chat ==========
    if chat.type == "private":
        if message.reply_to_message and message.reply_to_message.from_user:
            # Kalau reply ke orang di private chat
            replied = message.reply_to_message
            replied_user = replied.from_user
            text = f"""Message ID: <code>{message.id}</code>
Your ID: <code>{user.id}</code>
Chat ID: <code>{chat.id}</code>

Replied Message Information:
├ Message ID: <code>{replied.id}</code>
├ User ID: <code>{replied_user.id}</code>"""
        else:
            # Kalau tidak reply
            text = f"""Message ID: <code>{message.id}</code>
Your ID: <code>{user.id}</code>
Chat ID: <code>{chat.id}</code>"""

    # ========== Group/Channel ==========
    else:
        chat_title = chat.title or "Private Chat"
        username_text = f"@{user.username}" if user.username else "Tidak ada"
        digit_info = f"({len(str(user.id))} digit)"
        text = f"""
<b>✉️ Msg ID:</b> <code>{message.id}</code>
<b>👤 Nama:</b> {user.first_name}
<b>🔗 Username:</b> {username_text}
<b>🆔 User ID:</b> <code>{user.id}</code> {digit_info}
<b>💬 Chat ID:</b> <code>{chat.id}</code> ({chat_title})
"""

    await message.reply(text, quote=True)


# UBOT
@PY.UBOT("id|cekid|myid")
async def _(client, message):
    await cekid_handler(client, message)

# BOT
@PY.BOT("id|cekid|myid")
async def _(client, message):
    await cekid_handler(client, message)
