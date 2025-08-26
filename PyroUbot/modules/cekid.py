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

from pyrogram.enums import ChatType

async def cekid_handler(client, message):
    user = message.from_user
    chat = message.chat
    args = message.text.split(maxsplit=1)

    target_user = None

    # Kalau reply → ambil user dari reply
    if message.reply_to_message and message.reply_to_message.from_user:
        target_user = message.reply_to_message.from_user

    # Kalau pakai argumen → resolve username / user_id
    elif len(args) > 1:
        try:
            target_user = await client.get_users(args[1])
        except Exception as e:
            return await message.reply(f"❌ Tidak bisa menemukan user: <code>{args[1]}</code>\nError: {e}")

    # Default → user pengirim sendiri
    else:
        target_user = user

    # ========== Private Chat ==========
    if chat.type in [ChatType.PRIVATE, ChatType.BOT]:
        text = f"""Message ID: <code>{message.id}</code>
Your ID: <code>{user.id}</code>
Chat ID: <code>{chat.id}</code>

Target User Information:
├ Nama: {target_user.first_name}
├ User ID: <code>{target_user.id}</code>
├ Username: @{target_user.username if target_user.username else 'Tidak ada'}"""

    # ========== Group / Supergroup ==========
    elif chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        chat_title = chat.title or "Group"
        digit_info = f"({len(str(target_user.id))} digit)"
        text = f"""✉️ Msg ID: <code>{message.id}</code>
👤 Nama: {target_user.first_name}
🔗 Username: @{target_user.username if target_user.username else 'Tidak ada'}
🆔 User ID: <code>{target_user.id}</code> {digit_info}
💬 Chat ID: <code>{chat.id}</code> ({chat_title})"""

    # ========== Channel ==========
    elif chat.type == ChatType.CHANNEL:
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
