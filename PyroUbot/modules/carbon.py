import asyncio
import os
import requests

from asyncio import sleep
from pyrogram.raw.functions.messages import DeleteHistory, StartBot

from bs4 import BeautifulSoup
from io import BytesIO

from telegraph import Telegraph, exceptions, upload_file

from PyroUbot import *



__MODULE__ = "ᴄᴀʀʙᴏɴ"
__HELP__ = """
<b>⦪࿈ ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴄᴀʀʙᴏɴ ࿈⦫<b>

<blockquote><b>⎆ perintah :
ᚗ <code>{0}carbon</code>
⊷ membuat text carbonara

"""

@PY.UBOT("limit")
@PY.TOP_CMD
async def _(client, message):
    prs = await EMO.PROSES(client)
    pong = await EMO.PING(client)
    yubot = await EMO.UBOT(client)

    # Unblock dan start SpamBot
    await client.unblock_user("SpamBot")
    bot_info = await client.resolve_peer("SpamBot")
    msg = await message.reply(f"{prs}processing . . .")
    response = await client.invoke(
        StartBot(
            bot=bot_info,
            peer=bot_info,
            random_id=client.rnd_id(),
            start_param="start",
        )
    )
    await sleep(1)
    await msg.delete()

    # Ambil balasan dari SpamBot
    status = await client.get_messages("SpamBot", response.updates[1].message.id + 1) 
    if status and hasattr(status, "text"):
        teks_spambot = status.text.lower()

        if "dibatasi" in teks_spambot or "restricted" in teks_spambot or "limit" in teks_spambot:
            # Akun kena limit → kirim isi asli dari SpamBot
            text = f"""
<b>⌭ {pong} Status Akun : LIMIT 🚫</b>
{status.text}
<b> ~ ⭐{client.me.mention}</b>
"""
        else:
            # Akun tidak kena limit
            text = f"""
<blockquote><b>⌭ {pong} Status Akun : ✅ Tidak Dibatasi</b></blockquote>
✅ Kabar baik, akun anda tidak dibatasi.
Anda bebas, sebebas burung yang lepas.
<b> ~ ⭐{client.me.mention}</b>
"""
        await client.send_message(message.chat.id, text)
        # Hapus history SpamBot biar bersih
        return await client.invoke(DeleteHistory(peer=bot_info, max_id=0, revoke=True))
    else:
        return await message.reply("❌ Tidak bisa membaca status dari SpamBot.")

async def make_carbon(code):
    url = "https://carbonara.solopov.dev/api/cook"
    async with aiosession.post(url, json={"code": code}) as resp:
        image = BytesIO(await resp.read())
    image.name = "carbon.png"
    return image


@PY.UBOT("carbon")
@PY.TOP_CMD
async def carbon_func(client, message):
    text = (
        message.text.split(None, 1)[1]
        if len(
            message.command,
        )
        != 1
        else None
    )
    if message.reply_to_message:
        text = message.reply_to_message.text or message.reply_to_message.caption
    if not text:
        return await message.delete()
    ex = await message.reply("memproꜱeꜱ...")
    carbon = await make_carbon(text)
    await ex.edit("uploading...")
    await asyncio.gather(
        ex.delete(),
        client.send_photo(
            message.chat.id,
            carbon,
            caption=f"carboniꜱed by :{client.me.mention}",
        ),
    )
    carbon.close()


def qr_gen(content):
    return {
        "data": content,
        "config": {
            "body": "circle-zebra",
            "eye": "frame13",
            "eyeBall": "ball14",
            "erf1": [],
            "erf2": [],
            "erf3": [],
            "brf1": [],
            "brf2": [],
            "brf3": [],
            "bodyColor": "#000000",
            "bgColor": "#FFFFFF",
            "eye1Color": "#000000",
            "eye2Color": "#000000",
            "eye3Color": "#000000",
            "eyeBall1Color": "#000000",
            "eyeBall2Color": "#000000",
            "eyeBall3Color": "#000000",
            "gradientColor1": "",
            "gradientColor2": "",
            "gradientType": "linear",
            "gradientOnEyes": "true",
            "logo": "",
            "logoMode": "default",
        },
        "size": 1000,
        "download": "imageUrl",
        "file": "png",
    }


@PY.UBOT("qrgen")
@PY.TOP_CMD
async def _(client, message):
    ID = message.reply_to_message or message
    if message.reply_to_message:
        data = qr_gen(message.reply_to_message.text)
    else:
        if len(message.command) < 2:
            return await message.delete()
        else:
            data = qr_gen(message.text.split(None, 1)[1])
    Tm = await message.reply("sedang memproses buat qrcode....")
    try:
        QRcode = (
            requests.post(
                "https://api.qrcode-monkey.com//qr/custom",
                json=data,
            )
            .json()["imageUrl"]
            .replace("//api", "https://api")
        )
        await client.send_photo(message.chat.id, QRcode, reply_to_message_id=ID.id)
        await Tm.delete()
    except Exception as error:
        await Tm.edit(error)



@PY.UBOT("qrread")
@PY.TOP_CMD
async def _(client, message):
    replied = message.reply_to_message
    if not (replied and replied.media and (replied.photo or replied.sticker)):
        await message.reply("balas kode qr untuk mendapatkan data...")
        return
    if not os.path.isdir("premiumQR/"):
        os.makedirs("premiumQR/")
    AM = await message.reply("mengunduh media...")
    down_load = await client.download_media(message=replied, file_name="premiumQR/")
    await AM.edit("memproses kode qr anda...")
    cmd = [
        "curl",
        "-X",
        "POST",
        "-F",
        "f=@" + down_load + "",
        "https://zxing.org/w/decode",
    ]
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    out_response = stdout.decode().strip()
    err_response = stderr.decode().strip()
    os.remove(down_load)
    if not (out_response or err_response):
        await AM.edit("tidak bisa mendapatkan data kode qr ini...")
        return
    try:
        soup = BeautifulSoup(out_response, "html.parser")
        qr_contents = soup.find_all("pre")[0].text
    except IndexError:
        await AM.edit("indeks daftar di luar jangkauan")
        return
    await AM.edit(f"data qrcode:\n{qr_contents}")
  

@PY.UBOT("font")
@PY.TOP_CMD
async def _(client, message):
    if message.reply_to_message:
        if message.reply_to_message.text:
            query = id(message)
        else:
            return await message.reply("harap reply ke text")
    else:
        if len(message.command) < 2:
            return await message.reply(f"{message.text} [reply/text]")
        else:
            query = id(message)
    try:
        x = await client.get_inline_bot_results(bot.me.username, f"get_font {query}")
        return await message.reply_inline_bot_result(x.query_id, x.results[0].id)
    except Exception as error:
        return await message.reply(error)


@PY.INLINE("^get_font")
async def _(client, inline_query):
    get_id = int(inline_query.query.split(None, 1)[1])
    buttons = InlineKeyboard(row_width=3)
    keyboard = []
    for X in query_fonts[0]:
        keyboard.append(
            InlineKeyboardButton(X, callback_data=f"get {get_id} {query_fonts[0][X]}")
        )
    buttons.add(*keyboard)
    buttons.row(InlineKeyboardButton("►", callback_data=f"next {get_id}"))
    await client.answer_inline_query(
        inline_query.id,
        cache_time=0,
        results=[
            (
                InlineQueryResultArticle(
                    title="get font!",
                    reply_markup=buttons,
                    input_message_content=InputTextMessageContent(
                        "silahkan pilih salah satu font dibawah"
                    ),
                )
            )
        ],
    )


@PY.CALLBACK("^get")
async def _(client, callback_query):
    try:
        q = int(callback_query.data.split()[1])
        m = [obj for obj in get_objects() if id(obj) == q][0]
        new = str(callback_query.data.split()[2])
        if m.reply_to_message:
            text = m.reply_to_message.text
        else:
            text = m.text.split(None, 1)[1]
        get_new_font = gens_font(new, text)
        return await callback_query.edit_message_text(get_new_font)
    except Exception as error:
        return await callback_query.answer(f"Error: {error}", True)


@PY.CALLBACK("^next")
async def _(client, callback_query):
    try:
        get_id = int(callback_query.data.split()[1])
        buttons = InlineKeyboard(row_width=3)
        keyboard = []
        for X in query_fonts[1]:
            keyboard.append(
                InlineKeyboardButton(
                    X, callback_data=f"get {get_id} {query_fonts[1][X]}"
                )
            )
        buttons.add(*keyboard)
        buttons.row(InlineKeyboardButton("◄", callback_data=f"prev {get_id}"))
        return await callback_query.edit_message_reply_markup(reply_markup=buttons)
    except Exception as error:
        return await callback_query.answer(f"Error: {error}", True)


@PY.CALLBACK("^prev")
async def _(client, callback_query):
    try:
        get_id = int(callback_query.data.split()[1])
        buttons = InlineKeyboard(row_width=3)
        keyboard = []
        for X in query_fonts[0]:
            keyboard.append(
                InlineKeyboardButton(
                    X, callback_data=f"get {get_id} {query_fonts[0][X]}"
                )
            )
        buttons.add(*keyboard)
        buttons.row(InlineKeyboardButton("►", callback_data=f"next {get_id}"))
        return await callback_query.edit_message_reply_markup(reply_markup=buttons)
    except Exception as error:
        return await callback_query.answer(f"❌ Error: {error}", True)
