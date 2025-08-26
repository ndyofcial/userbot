import re
from pykeyboard import InlineKeyboard
from pyrogram.errors import MessageNotModified
from pyrogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle,
    InputTextMessageContent, ReplyKeyboardMarkup, KeyboardButton
)
from pyromod.helpers import ikb

from PyroUbot import *


def detect_url_links(text):
    link_pattern = r"(?:https?://)?(?:www\.)?[a-zA-Z0-9.-]+(?:\.[a-zA-Z]{2,})+(?:[/?]\S+)?"
    return re.findall(link_pattern, text)


def detect_button_and_text(text):
    button_matches = re.findall(r"\| ([^|]+) - ([^|]+) \|", text)
    text_matches = re.search(r"(.*?) \|", text, re.DOTALL).group(1) if "|" in text else text
    return button_matches, text_matches


def create_inline_keyboard(text, user_id=False, is_back=False):
    keyboard = []
    button_matches, text_matches = detect_button_and_text(text)

    prev_button_data = None
    for button_text, button_data in button_matches:
        data = (
            button_data.split("#")[0]
            if detect_url_links(button_data.split("#")[0])
            else f"_gtnote {int(user_id.split('_')[0])}_{user_id.split('_')[1]} {button_data.split('#')[0]}"
        )
        cb_data = data if user_id else button_data.split("#")[0]

        if "#" in button_data:
            if prev_button_data:
                if detect_url_links(cb_data):
                    keyboard[-1].append(InlineKeyboardButton(button_text, url=cb_data))
                else:
                    keyboard[-1].append(InlineKeyboardButton(button_text, callback_data=cb_data))
            else:
                button_row = [InlineKeyboardButton(button_text, url=cb_data)] if detect_url_links(cb_data) else [InlineKeyboardButton(button_text, callback_data=cb_data)]
                keyboard.append(button_row)
        else:
            button_row = [InlineKeyboardButton(button_text, url=cb_data)] if button_data.startswith("http") else [InlineKeyboardButton(button_text, callback_data=cb_data)]
            keyboard.append(button_row)

        prev_button_data = button_data

    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    if user_id and is_back:
        markup.inline_keyboard.append([
            InlineKeyboardButton("ᴋᴇᴍʙᴀʟɪ", f"_gtnote {int(user_id.split('_')[0])}_{user_id.split('_')[1]}")
        ])

    return markup, text_matches


class BTN:
    def ALIVE(get_id):
        return [
            [InlineKeyboardButton("ᴛᴜᴛᴜᴘ", callback_data=f"alv_cls {int(get_id[1])} {int(get_id[2])}")],
            [InlineKeyboardButton("ʜᴇʟᴘ", callback_data="help_back")]
        ]

    def BOT_HELP(message):
        return [
            [InlineKeyboardButton("ʀᴇsᴛᴀʀᴛ", callback_data="reboot")],
            [InlineKeyboardButton("ꜱʏꜱᴛᴇᴍ", callback_data="system")],
            [InlineKeyboardButton("ᴜʙᴏᴛ", callback_data="ubot")],
            [InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇ", callback_data="update")]
        ]

    def ADD_EXP(user_id):
        buttons = InlineKeyboard(row_width=3)
        keyboard = [
            InlineKeyboardButton(f"{X} ʙᴜʟᴀɴ ", callback_data=f"success {user_id} {X}") for X in range(1, 13)
        ]
        buttons.add(*keyboard)
        buttons.row(InlineKeyboardButton("⦪ ᴅᴀᴘᴀᴛᴋᴀɴ ᴘʀᴏfɪʟ ⦫", callback_data=f"profil {user_id}"))
        buttons.row(InlineKeyboardButton("⦪ ᴛᴏʟᴀᴋ ᴘᴇᴍʙᴀʏᴀʀᴀɴ ⦫", callback_data=f"failed {user_id}"))
        return buttons

    def EXP_UBOT():
        return [[InlineKeyboardButton("beli userbot", callback_data="bahan")]]

    def PLUS_MINUS(query, user_id):
        return [
            [
                InlineKeyboardButton("-1", callback_data=f"kurang {query}"),
                InlineKeyboardButton("+1", callback_data=f"tambah {query}")
            ],
            [InlineKeyboardButton("⦪ ᴋᴏɴꜰɪʀᴍᴀsɪ ⦫", callback_data="confirm")],
            [InlineKeyboardButton("⦪ ʙᴀᴛᴀʟᴋᴀɴ ⦫", callback_data=f"home {user_id}")]
        ]

    def UBOT(user_id, count):
        return [
            [InlineKeyboardButton("⦪ ʜᴀᴘᴜs ᴅᴀʀɪ ᴅᴀᴛᴀʙᴀsᴇ ⦫", callback_data=f"del_ubot {int(user_id)}")],
            [InlineKeyboardButton("⦪ ᴄᴇᴋ ᴍᴀsᴀ ᴀᴋᴛɪғ ⦫", callback_data=f"cek_masa_aktif {int(user_id)}")],
            [
                InlineKeyboardButton("⟢", callback_data=f"p_ub {int(count)}"),
                InlineKeyboardButton("⟣", callback_data=f"n_ub {int(count)}"),
            ]
        ]

    def DEAK(user_id, count):
        return [
            [
                InlineKeyboardButton("⦪ ᴋᴇᴍʙᴀʟɪ ⦫", callback_data=f"p_ub {int(count)}"),
                InlineKeyboardButton("⦪ sᴇᴛᴜᴊᴜɪ ⦫", callback_data=f"deak_akun {int(count)}"),
            ]
        ]


def START_KEYBOARD(user_id):
    if user_id != OWNER_ID:
        button = [
            [KeyboardButton("⦪ ᴛʀɪᴀʟ ⦫")],
            [KeyboardButton("⦪ ʙᴇʟɪ ᴜꜱᴇʀʙᴏᴛ ⦫"), KeyboardButton("⦪ ʀᴇsᴇᴛ ᴘʀᴇғɪx ⦫")],
            [KeyboardButton("⳹ ʀᴇᴘᴏ ᴜsᴇʀʙᴏᴛ ⳼"), KeyboardButton("⳹ ᴏᴡɴᴇʀ ⳼")],
            [KeyboardButton("⦪ ʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ ⦫"), KeyboardButton("⦪ ʜᴇʟᴘ ᴍᴇɴᴜ ⦫")],
            [KeyboardButton("⦪ sᴜᴘᴘᴏʀᴛ ⦫")]
        ]
    else:
        button = [
            [KeyboardButton("⦪ ʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ ⦫"), KeyboardButton("⦪ ʀᴇsᴇᴛ ᴘʀᴇғɪx ⦫")],
            [KeyboardButton("⦪ ɢɪᴛᴘᴜʟʟ ⦫"), KeyboardButton("⦪ ʀᴇsᴛᴀʀᴛ ⦫")],
            [KeyboardButton("⦪ ʟɪsᴛ ᴜsᴇʀʙᴏᴛ ⦫")]
        ]
    return ReplyKeyboardMarkup(button, resize_keyboard=True)


class INLINE:
    def QUERY(func):
        async def wrapper(client, inline_query):
            users = ubot._get_my_id
            if inline_query.from_user.id not in users:
                await client.answer_inline_query(
                    inline_query.id,
                    cache_time=1,
                    results=[
                        InlineQueryResultArticle(
                            title=f"ᴀɴᴅᴀ ʙᴇʟᴜᴍ ᴏʀᴅᴇʀ @{bot.me.username}",
                            input_message_content=InputTextMessageContent(
                                f"sɪʟᴀʜᴋᴀɴ ᴏʀᴅᴇʀ ᴅɪ @{bot.me.username} ᴅᴜʟᴜ ʙɪᴀʀ ʙɪsᴀ ᴍᴇɴɢɢᴜɴᴀᴋᴀɴ ɪɴʟɪɴᴇ ɪɴɪ"
                            ),
                        )
                    ],
                )
            else:
                await func(client, inline_query)
        return wrapper

    def DATA(func):
        async def wrapper(client, callback_query):
            users = ubot._get_my_id
            if callback_query.from_user.id not in users:
                await callback_query.answer(
                    f"ᴍᴀᴋᴀɴʏᴀ ᴏʀᴅᴇʀ ᴜsᴇʀʙᴏᴛ @{bot.me.username} ᴅᴜʟᴜ ʙɪᴀʀ ʙɪsᴀ ᴋʟɪᴋ ᴛᴏᴍʙᴏʟ ɪɴɪ",
                    True,
                )
            else:
                try:
                    await func(client, callback_query)
                except MessageNotModified:
                    await callback_query.answer("❌ ERROR")
        return wrapper


async def create_button(m):
    buttons = InlineKeyboard(row_width=1)
    keyboard = []
    msg = []
    if "-/" not in m.text.split(None, 1)[1]:
        for X in m.text.split(None, 1)[1].split():
            X_parts = X.split(":", 1)
            keyboard.append(InlineKeyboardButton(X_parts[0].replace("_", " "), url=X_parts[1]))
            msg.append(X_parts[0])
        buttons.add(*keyboard)
        text = m.reply_to_message.text if m.reply_to_message else " ".join(msg)
    else:
        for X in m.text.split("-/", 1)[1].split():
            X_parts = X.split(":", 1)
            keyboard.append(InlineKeyboardButton(X_parts[0].replace("_", " "), url=X_parts[1]))
        buttons.add(*keyboard)
        text = m.text.split("-/", 1)[0].split(None, 1)[1]
    return buttons, text


async def notes_create_button(text):
    buttons = InlineKeyboard(row_width=2)
    keyboard = []
    split_text = text.split("-/", 1)
    for X in split_text[1].split():
        split_X = X.split(":", 1)
        button_text = split_X[0].replace("_", " ")
        button_url = split_X[1]
        keyboard.append(InlineKeyboardButton(button_text, url=button_url))
    buttons.add(*keyboard)
    return buttons, split_text[0]
