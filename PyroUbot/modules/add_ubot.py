import asyncio
import importlib
from datetime import datetime

from pyrogram.enums import SentCodeType
from pyrogram.errors import *
from pyrogram.types import *
from pyrogram.raw import functions

from PyroUbot import *


# Start handler
@PY.BOT("start")
@PY.START
@PY.PRIVATE
async def _(client, message):
    user_id = message.from_user.id

    if user_id != OWNER_ID:
        buttons = [
            [KeyboardButton("⦪ ᴛʀɪᴀʟ ⦫")],
            [KeyboardButton("⦪ ʙᴇʟɪ ᴜꜱᴇʀʙᴏᴛ ⦫"), KeyboardButton("⦪ ʀᴇsᴇᴛ ᴘʀᴇғɪx ⦫")],
            [KeyboardButton("⳹ ʀᴇᴘᴏ ᴜsᴇʀʙᴏᴛ ⳼"), KeyboardButton("⳹ ᴏᴡɴᴇʀ ⳼")],
            [KeyboardButton("⦪ ʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ ⳼"), KeyboardButton("⦪ ʜᴇʟᴘ ᴍᴇɴᴜ ⦫")],
            [KeyboardButton("⦪ sᴜᴘᴘᴏʀᴛ ⦫"), KeyboardButton("⦪ ʟɪsᴛ ᴜsᴇʀʙᴏᴛ ⦫")]
        ]
    else:
        buttons = [
            [KeyboardButton("⦪ ʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ ⦫"), KeyboardButton("⦪ ʀᴇsᴇᴛ ᴘʀᴇғɪx ⦫")],
            [KeyboardButton("⦪ ɢɪᴛᴘᴜʟʟ ⦫"), KeyboardButton("⦪ ʀᴇsᴛᴀʀᴛ ⦫")],
            [KeyboardButton("⦪ ʟɪsᴛ ᴜsᴇʀʙᴏᴛ ⦫")]
        ]

    reply_markup = ReplyKeyboardMarkup(
        buttons,
        resize_keyboard=True,
        one_time_keyboard=False
    )

    msg = MSG.START(message)
    await message.reply_video(
        "https://files.catbox.moe/axrb4w.mp4",
        caption=msg,
        reply_markup=reply_markup
    )

# Handler teks untuk ReplyKeyboard
@PY.BOT("text")
async def handle_text(client, message):
    text = message.text
    user_id = message.from_user.id

    # Tombol ReplyKeyboard lainnya
    if text == "⦪ ᴛʀɪᴀʟ ⦫":
        await message.reply("Menjalankan TRIAL...")
    elif text == "⦪ ʙᴇʟɪ ᴜꜱᴇʀʙᴏᴛ ⦫":
        await message.reply("Menjalankan BELI USERBOT...")
    elif text == "⦪ ʀᴇsᴇᴛ ᴘʀᴇғɪx ⦫":
        await message.reply("Menjalankan RESET PREFIX...")
    elif text == "⳹ ʀᴇᴘᴏ ᴜsᴇʀʙᴏᴛ ⳼":
        await message.reply("Link repo: t.me/moire_marketx")
    elif text == "⳹ ᴏᴡɴᴇʀ ⳼":
        await message.reply("Link owner: t.me/moire_mor")
    elif text == "⦪ ʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ ⳼" or text == "⦪ ʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ ⦫":
        await message.reply("Menjalankan BUAT USERBOT...")
    elif text == "⦪ ʜᴇʟᴘ ᴍᴇɴᴜ ⦫":
        await message.reply("Menjalankan HELP MENU...")
    elif text == "⦪ sᴜᴘᴘᴏʀᴛ ⦫":
        await message.reply("Menjalankan SUPPORT...")
    elif text == "⦪ ɢɪᴛᴘᴜʟʟ ⦫":
        await message.reply("Menjalankan GITPULL...")
    elif text == "⦪ ʀᴇsᴛᴀʀᴛ ⦫":
        await message.reply("Menjalankan RESTART...")

    # Tombol List Userbot → memanggil InlineKeyboard versi cek_ubot
    if text == "⦪ ʟɪsᴛ ᴜsᴇʀʙᴏᴛ ⦫":
        if not ubot._ubot:
            return await message.reply("<b>⎆ Belum ada userbot terdaftar.</b>")
        
        index = 0  # mulai dari userbot pertama
        ubot_text = await MSG.UBOT(index)
        markup = InlineKeyboardMarkup(BTN.UBOT(ubot._ubot[index].me.id, index))
        await message.reply(ubot_text, reply_markup=markup)


@PY.CALLBACK("bahan")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id in ubot._get_my_id:
        buttons = [
            [InlineKeyboardButton("⦪ ʀᴇꜱᴛᴀʀᴛ ⦫", callback_data=f"ress_ubot")],
            [InlineKeyboardButton("⦪ ᴋᴇᴍʙᴀʟɪ ⦫", callback_data=f"home {user_id}")],
        ]
        return await callback_query.edit_message_text(
            f"""
<blockquote><b>⌭ ᴀɴᴅᴀ ꜱᴜᴅᴀʜ ᴍᴇᴍʙᴜᴀᴛ ᴜꜱᴇʀʙᴏᴛ\n\n⌭ ᴊɪᴋᴀ ᴜꜱᴇʀʙᴏᴛ ᴀɴᴅᴀ ᴛɪᴅᴀᴋ ʙɪꜱᴀ ᴅɪɢᴜɴᴀᴋᴀɴ ꜱɪʟᴀʜᴋᴀɴ ᴛᴇᴋᴇɴ ᴛᴏᴍʙᴏʟ ʀᴇꜱᴛᴀʀᴛ ᴅɪ ᴀᴛᴀꜱ</b></blockquote>
""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    elif len(ubot._ubot) + 1 > MAX_BOT:
        buttons = [
            [InlineKeyboardButton("ᴋᴇᴍʙᴀʟɪ", callback_data=f"home {user_id}")],
        ]
        return await callback_query.edit_message_text(
            f"""
<blockquote><b><b>☫ ᴛɪᴅᴀᴋ ʙɪsᴀ ᴍᴇᴍʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ!</b>

<b>☫ ᴋᴀʀᴇɴᴀ ᴍᴀᴋsɪᴍᴀʟ ᴜsᴇʀʙᴏᴛ ᴀᴅᴀʟᴀʜ {Fonts.smallcap(str(len(ubot._ubot)))} ᴛᴇʟᴀʜ ᴛᴇʀᴄᴀᴘᴀɪ</b>

<blockquote><b>☫ sɪʟᴀʜᴋᴀɴ ʜᴜʙᴜɴɢɪ owner</b></blockquote>
""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    premium_users, ultra_premium_users = await get_list_from_vars(client.me.id, "PREM_USERS"), await get_list_from_vars(client.me.id, "ULTRA_PREM")
    if user_id not in premium_users and user_id not in ultra_premium_users:
        buttons = [
            [InlineKeyboardButton("⦪ ʟᴀɴᴊᴜᴛᴋᴀɴ ⦫", callback_data="bayar_dulu")],
            [InlineKeyboardButton("⦪ ᴋᴇᴍʙᴀʟɪ ⦫", callback_data=f"home {user_id}")],
        ]
        return await callback_query.edit_message_text(
            MSG.POLICY(),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        buttons = [[InlineKeyboardButton("⦪ ʟᴀɴᴊᴜᴛᴋᴀɴ ⦫", callback_data="add_ubot")]]
        return await callback_query.edit_message_text(
            """
<blockquote><b>⌭ ᴀɴᴅᴀ ᴛᴇʟᴀʜ ᴍᴇᴍʙᴇʟɪ ᴜꜱᴇʀʙᴏᴛ ꜱɪʟᴀʜᴋᴀɴ ᴘᴇɴᴄᴇᴛ ᴛᴏᴍʙᴏʟ ʟᴀɴᴊᴜᴛᴋᴀɴ ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴜᴀᴛ ᴜꜱᴇʀʙᴏᴛ</b></blockquote>
""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )


@PY.CALLBACK("status")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id in ubot._get_my_id:
        buttons = [
            [InlineKeyboardButton("ᴋᴇᴍʙᴀʟɪ", callback_data=f"home {user_id}")],
        ]
        exp = await get_expired_date(user_id)
        prefix = await get_pref(user_id)
        waktu = exp.strftime("%d-%m-%Y") if exp else "None"
        return await callback_query.edit_message_text(
            f"""
<blockquote>⌬ ᴜꜱᴇʀʙᴏᴛ ᴘʀᴇᴍɪᴜᴍ
  ᚗ ꜱᴛᴀᴛᴜꜱ : ᴘʀᴇᴍɪᴜᴍ
  ᚗ ᴘʀᴇꜰɪxᴇꜱ : {prefix[0]}
  ᚗ ᴇxᴘɪʀᴇᴅ_ᴏɴ : {waktu}</b></blockquote>
""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        buttons = [
            [InlineKeyboardButton("✮ ʙᴇʟɪ ᴜꜱᴇʀʙᴏᴛ ✮", callback_data=f"bahan")],
            [InlineKeyboardButton("⦪ ᴋᴇᴍʙᴀʟɪ ⦫", callback_data=f"home {user_id}")],
        ]
        return await callback_query.edit_message_text(
            f"""
<blockquote><b>☫ ᴍᴀᴀꜰ ᴀɴᴅᴀ ʙᴇʟᴜᴍ ᴍᴇᴍʙᴇʟɪ ᴜꜱᴇʀʙᴏᴛ, ꜱɪʟᴀᴋᴀɴ ᴍᴇᴍʙᴇʟɪ ᴛᴇʀʟᴇʙɪʜ ᴅᴀʜᴜʟᴜ.</b></blockquote>
""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
    )


@PY.CALLBACK("buat_ubot")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id in ubot._get_my_id:
        buttons = [
            [InlineKeyboardButton("⦪ ʀᴇꜱᴛᴀʀᴛ ⦫", callback_data=f"ress_ubot")],
            [InlineKeyboardButton("⦪ ᴋᴇᴍʙᴀʟɪ ⦫", callback_data=f"home {user_id}")],
        ]
        return await callback_query.edit_message_text(
            f"""
<blockquote><b>⌭ ᴀɴᴅᴀ ꜱᴜᴅᴀʜ ᴍᴇᴍʙᴜᴀᴛ ᴜꜱᴇʀʙᴏᴛ\n\n⌭ ᴊɪᴋᴀ ᴜꜱᴇʀʙᴏᴛ ᴀɴᴅᴀ ᴛɪᴅᴀᴋ ʙɪꜱᴀ ᴅɪɢᴜɴᴀᴋᴀɴ ꜱɪʟᴀʜᴋᴀɴ ᴛᴇᴋᴇɴ ᴛᴏᴍʙᴏʟ ʀᴇꜱᴛᴀʀᴛ ᴅɪ ᴀᴛᴀꜱ</b></blockquote>
""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    elif len(ubot._ubot) + 1 > MAX_BOT:
        buttons = [
            [InlineKeyboardButton("ᴋᴇᴍʙᴀʟɪ", callback_data=f"home {user_id}")],
        ]
        return await callback_query.edit_message_text(
            f"""
<blockquote><b><b>⌬ ᴛɪᴅᴀᴋ ʙɪsᴀ ᴍᴇᴍʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ!</b>

<b>⌬ ᴋᴀʀᴇɴᴀ ᴍᴀᴋsɪᴍᴀʟ ᴜsᴇʀʙᴏᴛ ᴀᴅᴀʟᴀʜ {Fonts.smallcap(str(len(ubot._ubot)))} ᴛᴇʟᴀʜ ᴛᴇʀᴄᴀᴘᴀɪ</b>

<blockquote><b>⌬ sɪʟᴀʜᴋᴀɴ ʜᴜʙᴜɴɢɪ: ᴀᴅᴍɪɴ ᴊɪᴋᴀ ᴍᴀᴜ ᴅɪʙᴜᴀᴛᴋᴀɴ ʙᴏᴛ sᴇᴘᴇʀᴛɪ sᴀʏᴀ </b></blockquote>
""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    premium_users, ultra_premium_users = await get_list_from_vars(client.me.id, "PREM_USERS"), await get_list_from_vars(client.me.id, "ULTRA_PREM")
    if user_id not in premium_users and user_id not in ultra_premium_users:
        buttons = [
            [InlineKeyboardButton("⦪ ʙᴇʟɪ ᴜꜱᴇʀʙᴏᴛ ⦫", callback_data="bahan")],
            [InlineKeyboardButton("⦪ ᴋᴇᴍʙᴀʟɪ ⦫", callback_data=f"home {user_id}")],
        ]
        return await callback_query.edit_message_text(
            f"""
<blockquote><b>⌬ ᴍᴀᴀꜰ ᴀɴᴅᴀ ʙᴇʟᴜᴍ ᴍᴇᴍʙᴇʟɪ ᴜꜱᴇʀʙᴏᴛ, ꜱɪʟᴀᴋᴀɴ ᴍᴇᴍʙᴇʟɪ ᴛᴇʀʟᴇʙɪʜ ᴅᴀʜᴜʟᴜ</b></blockquote>
""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )


@PY.CALLBACK("bayar_dulu")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    buttons = BTN.PLUS_MINUS(1, user_id)
    return await callback_query.edit_message_text(
        MSG.TEXT_PAYMENT(30, 30, 1),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@PY.CALLBACK("add_ubot")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    await callback_query.message.delete()

    # tombol share contact
    keyboard = ReplyKeyboardMarkup(
        [[KeyboardButton("📞Kontak Saya", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    msg = await bot.send_message(
        user_id,
        "<blockquote><b>Silahkan klik tombol 📞 Kontak Saya untuk mengirimkan Nomor Telepon Telegram Anda.</b></blockquote>",
        reply_markup=keyboard
    )

    try:
        phone = await bot.listen(user_id, timeout=300)  # tunggu kontak
    except asyncio.TimeoutError:
        return await bot.send_message(
            user_id,
            "<blockquote>⎆ Pem-batalan otomatis!\n⎆ Gunakan /start untuk memulai ulang</blockquote>"
        )

    if not phone.contact or not phone.contact.phone_number:
        return await bot.send_message(
            user_id,
        "<blockquote><b>Silahkan klik tombol 📞 Kontak Saya untuk mengirimkan Nomor Telepon Telegram Anda.</b></blockquote>"
        )

    phone_number = phone.contact.phone_number
    await msg.delete()

    # Buat client baru
    new_client = Ubot(
        name=str(callback_query.id),
        api_id=API_ID,
        api_hash=API_HASH,
        in_memory=False,
    )

    get_otp = await bot.send_message(user_id, "<blockquote><b>⎆ Mengirim kode OTP...</b></blockquote>")
    await new_client.connect()

    try:
        code = await new_client.send_code(phone_number.strip())
    except ApiIdInvalid as e:
        await get_otp.delete()
        return await bot.send_message(user_id, e)
    except PhoneNumberInvalid as e:
        await get_otp.delete()
        return await bot.send_message(user_id, e)
    except PhoneNumberFlood as e:
        await get_otp.delete()
        return await bot.send_message(user_id, e)
    except PhoneNumberBanned as e:
        await get_otp.delete()
        return await bot.send_message(user_id, e)
    except PhoneNumberUnoccupied as e:
        await get_otp.delete()
        return await bot.send_message(user_id, e)
    except Exception as e:
        await get_otp.delete()
        return await bot.send_message(user_id, f"ERROR: {e}")

    try:
        sent_code = {
            SentCodeType.APP: "<a href=tg://openmessage?user_id=777000>akun Telegram resmi</a>",
            SentCodeType.SMS: "SMS Anda",
            SentCodeType.CALL: "panggilan telepon",
            SentCodeType.FLASH_CALL: "panggilan kilat",
            SentCodeType.FRAGMENT_SMS: "fragment SMS",
            SentCodeType.EMAIL_CODE: "email Anda",
        }
        await get_otp.delete()
        otp = await bot.ask(
            user_id,
            (
                "<blockquote><b>Silakan Periksa Kode OTP dari <a href='tg://openmessage?user_id=777000'>Akun Telegram Resmi</a>. Kirim Kode OTP ke sini setelah membaca Format di bawah ini.\n"
                "\nJika Kode OTP adalah 12345 Tolong [ TAMBAHKAN SPASI ] kirimkan Seperti ini 1 2 3 4 5.</b></blockquote>"
            ),
            timeout=300,
        )
    except asyncio.TimeoutError:
        return await bot.send_message(user_id, "<blockquote>⎆ Pem-batalan otomatis!\n⎆ Gunakan /start untuk memulai ulang</blockquote>")

    if await is_cancel(callback_query, otp.text):
        return

    otp_code = otp.text
    try:
        await new_client.sign_in(
            phone_number.strip(),
            code.phone_code_hash,
            phone_code=" ".join(str(otp_code)),
        )
    except PhoneCodeInvalid as e:
        return await bot.send_message(user_id, e)
    except PhoneCodeExpired as e:
        return await bot.send_message(user_id, e)
    except BadRequest as e:
        return await bot.send_message(user_id, f"ERROR: {e}")
    except SessionPasswordNeeded:
        try:
            two_step_code = await bot.ask(
                user_id,
                "⎆ Akun Anda mengaktifkan verifikasi dua langkah. Kirim password Anda.\n\nGunakan /cancel untuk batal.",
                timeout=300,
            )
        except asyncio.TimeoutError:
            return await bot.send_message(user_id, "<blockquote>⎆ Pem-batalan otomatis!\n⎆ Gunakan /start untuk memulai ulang</blockquote>")

        if await is_cancel(callback_query, two_step_code.text):
            return

        try:
            await new_client.check_password(two_step_code.text)
        except Exception as e:
            return await bot.send_message(user_id, f"ERROR: {e}")

    # simpan session
    session_string = await new_client.export_session_string()
    await new_client.disconnect()
    new_client.storage.session_string = session_string
    new_client.in_memory = False

    bot_msg = await bot.send_message(
        user_id,
        "⎆ Sedang memproses....\n\nMohon tunggu sebentar.",
        disable_web_page_preview=True,
    )

    await new_client.start()
    if not user_id == new_client.me.id:
        ubot._ubot.remove(new_client)
        return await bot_msg.edit(
            "<b>⎆ Harap gunakan nomor Telegram Anda sendiri, bukan akun lain.</b>"
        )

    await add_ubot(
        user_id=int(new_client.me.id),
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=session_string,
    )

    for mod in loadModule():
        importlib.reload(importlib.import_module(f"PyroUbot.modules.{mod}"))

    SH = await ubot.get_prefix(new_client.me.id)
    buttons = [[InlineKeyboardButton("ᴋᴇᴍʙᴀʟɪ", callback_data=f"home {user_id}")]]
    text_done = f"""
<blockquote><b>⎆ Berhasil diaktifkan
• Nama : <a href=tg://user?id={new_client.me.id}>{new_client.me.first_name} {new_client.me.last_name or ''}</a>
• ID : {new_client.me.id}
• Prefixes : {' '.join(SH)}
⌭ Hubungi admin untuk info terbaru
Jika bot tidak respon, ketik /restart</b></blockquote>
    """
    await bot_msg.edit(text_done, disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup(buttons))

    await bash("rm -rf *session*")
    await install_my_peer(new_client)

    try:
        await new_client.join_chat("rompublicvin2")
        await new_client.join_chat("averixnotif")
        await new_client.join_chat("ndytestimoni3")
        await new_client.join_chat("roomndy1")
        await new_client.join_chat("roomndy2")
    except UserAlreadyParticipant:
        pass

    return await bot.send_message(
        LOGS_MAKER_UBOT,
        f"""
<b>⌬ Userbot Diaktifkan</b>
<b> ├ Akun:</b> <a href=tg://user?id={new_client.me.id}>{new_client.me.first_name} {new_client.me.last_name or ''}</a> 
<b> ╰ ID:</b> <code>{new_client.me.id}</code>
""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("⦪ Cek Masa Aktif ⦫", callback_data=f"cek_masa_aktif {new_client.me.id}")]]
        ),
        disable_web_page_preview=True,
    )

async def is_cancel(callback_query, text):
    if text.startswith("/cancel"):
        await bot.send_message(
            callback_query.from_user.id, "<blockquote>⎆ ᴘᴇᴍʙᴀᴛᴀʟᴀɴ ᴏᴛᴏᴍᴀᴛɪꜱ!\n⎆ɢᴜɴᴀᴋᴀɴ /ꜱᴛᴀʀᴛ ᴜɴᴛᴜᴋ ᴍᴇᴍᴜʟᴀɪ ᴜʟᴀɴɢ</blockquote>"
        )
        return True
    return False


@PY.BOT("control")
async def _(client, message):
    buttons = [
            [InlineKeyboardButton("ʀᴇꜱᴛᴀʀᴛ", callback_data=f"ress_ubot")],
        ]
    await message.reply(
            f"""
<blockquote><b>⎆ ᴀɴᴅᴀ ᴀᴋᴀɴ ᴍᴇʟᴀᴋᴜᴋᴀɴ ʀᴇꜱᴛᴀʀᴛ?!\n⎆ ᴊɪᴋᴀ ɪʏᴀ ᴘᴇɴᴄᴇᴛ ᴛᴏᴍʙᴏʟ ᴅɪ ʙᴀᴡᴀʜ ɪɴɪ</b></blockquote>
""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )

@PY.CALLBACK("ress_ubot")
async def _(client, callback_query):
    if callback_query.from_user.id not in ubot._get_my_id:
        return await callback_query.answer(
            f"you don't have acces",
            True,
        )
    for X in ubot._ubot:
        if callback_query.from_user.id == X.me.id:
            for _ubot_ in await get_userbots():
                if X.me.id == int(_ubot_["name"]):
                    try:
                        ubot._ubot.remove(X)
                        ubot._get_my_id.remove(X.me.id)
                        UB = Ubot(**_ubot_)
                        await UB.start()
                        for mod in loadModule():
                            importlib.reload(
                                importlib.import_module(f"PyroUbot.modules.{mod}")
                            )
                        return await callback_query.edit_message_text(
                            f"⎆ ʀᴇꜱᴛᴀʀᴛ ʙᴇʀʜᴀꜱɪʟ ᴅɪʟᴀᴋᴜᴋᴀɴ !\n\n ⎆ ɴᴀᴍᴇ: {UB.me.first_name} {UB.me.last_name or ''} | {UB.me.id}"
                        )
                    except Exception as error:
                        return await callback_query.edit_message_text(f"{error}")

@PY.BOT("restart")
async def _(client, message):
    msg = await message.reply("<b>⎆ ᴛᴜɴɢɢᴜ sᴇʙᴇɴᴛᴀʀ</b>")
    if message.from_user.id not in ubot._get_my_id:
        return await msg.edit(
            f"you don't have acces",
            True,
        )
    for X in ubot._ubot:
        if message.from_user.id == X.me.id:
            for _ubot_ in await get_userbots():
                if X.me.id == int(_ubot_["name"]):
                    try:
                        ubot._ubot.remove(X)
                        ubot._get_my_id.remove(X.me.id)
                        UB = Ubot(**_ubot_)
                        await UB.start()
                        for mod in loadModule():
                            importlib.reload(
                                importlib.import_module(f"PyroUbot.modules.{mod}")
                            )
                        return await msg.edit(
                            f"⎆ ʀᴇꜱᴛᴀʀᴛ ʙᴇʀʜᴀꜱɪʟ ᴅɪʟᴀᴋᴜᴋᴀɴ !\n\n ⎆ ɴᴀᴍᴇ: {UB.me.first_name} {UB.me.last_name or ''} | `{UB.me.id}`"
                        )
                    except Exception as error:
                        return await msg.edit(f"{error}")


@PY.CALLBACK("cek_ubot")
@PY.BOT("getubot")
@PY.ADMIN
async def _(client, callback_query):
    if not ubot._ubot:
        return await callback_query.answer("⎆ Belum ada userbot terdaftar", True)
    
    index = 0
    await bot.send_message(
        callback_query.from_user.id,
        await MSG.UBOT(index),
        reply_markup=InlineKeyboardMarkup(BTN.UBOT(ubot._ubot[index].me.id, index)),
    )


@PY.CALLBACK("cek_masa_aktif")
async def _(client, callback_query):
    user_id = int(callback_query.data.split()[1])
    expired = await get_expired_date(user_id)
    try:
        xxxx = (expired - datetime.now()).days
        return await callback_query.answer(f"⎆ ᴛɪɴɢɢᴀʟ {xxxx} ʜᴀʀɪ ʟᴀɢɪ", True)
    except:
        return await callback_query.answer("⎆ sᴜᴅᴀʜ ᴛɪᴅᴀᴋ ᴀᴋᴛɪғ", True)

@PY.CALLBACK("del_ubot")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id not in await get_list_from_vars(client.me.id, "ADMIN_USERS"):
        return await callback_query.answer(
            f"❌ ᴛᴏᴍʙᴏʟ ɪɴɪ ʙᴜᴋᴀɴ ᴜɴᴛᴜᴋ ᴍᴜ {callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}",
            True,
        )
    try:
        show = await bot.get_users(callback_query.data.split()[1])
        get_id = show.id
        get_mention = f"{get_id}"
    except Exception:
        get_id = int(callback_query.data.split()[1])
        get_mention = f"{get_id}"
    for X in ubot._ubot:
        if get_id == X.me.id:
            await X.unblock_user(bot.me.username)
            await remove_ubot(X.me.id)
            ubot._get_my_id.remove(X.me.id)
            ubot._ubot.remove(X)
            await X.log_out()
            await callback_query.answer(
                f"⎆ {get_mention} ʙᴇʀʜᴀsɪʟ ᴅɪʜᴀᴘᴜs ᴅᴀʀɪ ᴅᴀᴛᴀʙᴀsᴇ", True
            )
            await callback_query.edit_message_text(
                await MSG.UBOT(0),
                reply_markup=InlineKeyboardMarkup(
                    BTN.UBOT(ubot._ubot[0].me.id, 0)
                ),
            )
            await bot.send_message(
                X.me.id,
                MSG.EXP_MSG_UBOT(X),
                reply_markup=InlineKeyboardMarkup(BTN.EXP_UBOT()),
            )

    
@PY.CALLBACK("^(p_ub|n_ub)$")
async def navigate_userbot(client, callback_query):
    if not ubot._ubot:
        return await callback_query.answer("⎆ Belum ada userbot aktif", True)

    data = callback_query.data.split()
    action = data[0]
    count = int(data[1])

    if action == "n_ub":
        count = (count + 1) % len(ubot._ubot)
    elif action == "p_ub":
        count = (count - 1) % len(ubot._ubot)

    ubot_text = await MSG.UBOT(count)
    markup = InlineKeyboardMarkup(BTN.UBOT(ubot._ubot[count].me.id, count))
    await callback_query.edit_message_text(
        ubot_text,
        reply_markup=markup,
        disable_web_page_preview=True
    )
