from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pytz import timezone
from PyroUbot.config import OWNER_ID
from PyroUbot import *



@PY.UBOT("prem")
async def _(client, message):
    user = message.from_user

    # Ambil list seller, admin & superultra
    seles_users = [int(x) for x in await get_list_from_vars(client.me.id, "SELER_USERS")]
    admin_users = [int(x) for x in await get_list_from_vars(client.me.id, "ADMIN_USERS")]
    superultra_users = [int(x) for x in await get_list_from_vars(client.me.id, "ULTRA_PREM")]

    # Gabungkan semua role
    allowed_users = set(seles_users + admin_users + superultra_users + [OWNER_ID])

    if user.id not in allowed_users:
        return

    # Ambil target & durasi
    reply = message.reply_to_message
    if reply:
        target_id = reply.from_user.id
        args = message.text.split(maxsplit=1)
        duration = args[1].lower() if len(args) > 1 else "1b"
    else:
        args = message.text.split()[1:]
        if not args:
            return await message.reply("""⛔ Cara penggunaan: `.prem user_id/username waktu`
Contoh:
- `.prem 1234567890 1b`
- `.prem @username 15h`
- Reply ke pesan user: `.prem 1b`
- `.prem 1234567890 0` → permanen (hanya owner)
""")
        target_id = args[0]
        duration = args[1].lower() if len(args) > 1 else "1b"

    # Normalisasi target_id
    if str(target_id).isdigit():
        target_id = int(target_id)

    # Cek permanen
    is_permanent = duration in ["0", "perma", "permanen"]

    if is_permanent:
        if user.id != OWNER_ID:
            return await message.reply("⛔ Hanya OWNER yang bisa memberikan premium permanen.")
        total_days = None  # permanen
    else:
        # Konversi ke hari
        if duration.endswith("b"):  # bulan
            total_days = int(duration[:-1]) * 30 if duration[:-1].isdigit() else 30
        elif duration.endswith("h"):  # hari
            total_days = int(duration[:-1]) if duration[:-1].isdigit() else 1
        else:
            total_days = 30

        # Tentukan maksimal hari berdasarkan role
        if user.id == OWNER_ID:
            max_days = 3650
        elif user.id in admin_users:
            max_days = 180
        elif user.id in seles_users:
            max_days = 90
        elif user.id in superultra_users:
            max_days = 365
        else:
            return await message.reply("⛔ Kamu tidak punya akses ke perintah ini.")

        if total_days > max_days:
            return await message.reply(f"⛔ Maksimal kamu hanya bisa memberikan {max_days} hari.")

    msg = await message.reply("⏳ Memproses...")

    try:
        target_user = await client.get_users(target_id)
    except Exception as e:
        return await msg.edit(f"❌ Error: {e}")

    try:
        tz = timezone("Asia/Jakarta")
        now = datetime.now(tz)

        if is_permanent:
            expired_date = None
            expired_str = "♾️ PERMANEN"
        else:
            dataexp = await get_expired_date(target_user.id)
            if dataexp and dataexp.tzinfo is None:
                dataexp = tz.localize(dataexp)

            if dataexp and dataexp > now:
                expired_date = dataexp + timedelta(days=total_days)
            else:
                expired_date = now + timedelta(days=total_days)

            expired_str = expired_date.strftime("%d-%m-%Y %H:%M")

        # Simpan expired baru
        await set_expired_date(target_user.id, expired_date)

        # Cegah duplikat PREM_USERS
        prem_users = await get_list_from_vars(client.me.id, "PREM_USERS")
        if str(target_user.id) not in prem_users:
            await add_to_vars(client.me.id, "PREM_USERS", target_user.id)

        await msg.edit(f"""
**👤 Nama:** {target_user.first_name}
🆔 ID: `{target_user.id}`
📚 Keterangan: Premium Aktif
⏳ Masa Aktif: {expired_str}
🔹 Silakan buka @{client.me.username} untuk menggunakan userbot
""")

        # Notif owner
        await client.send_message(
            OWNER_ID,
            f"""
**👤 Seller/Admin:** {message.from_user.first_name} (`{message.from_user.id}`)
**👤 Customer:** {target_user.first_name} (`{target_user.id}`)
⏳ Expired: `{expired_str}`
""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("⁉️ Seller/Admin", callback_data=f"profil {message.from_user.id}"),
                        InlineKeyboardButton("Customer ⁉️", callback_data=f"profil {target_user.id}"),
                    ],
                ]
            ),
        )

    except Exception as error:
        return await msg.edit(f"❌ Error: {error}")


@PY.UBOT("unprem")
async def _(client, message):
    user = message.from_user

    # Ambil list seller, admin & superultra
    seles_users = [int(x) for x in await get_list_from_vars(client.me.id, "SELER_USERS")]
    admin_users = [int(x) for x in await get_list_from_vars(client.me.id, "ADMIN_USERS")]
    superultra_users = [int(x) for x in await get_list_from_vars(client.me.id, "ULTRA_PREM")]

    # Gabungkan semua role
    allowed_users = set(seles_users + admin_users + superultra_users + [OWNER_ID])

    if user.id not in allowed_users:
        return  # selain role ini, gak bisa pakai /unprem

    msg = await message.reply("⏳ Memproses...")

    # Ambil target user
    reply = message.reply_to_message
    if reply:
        target_id = reply.from_user.id
    else:
        args = message.text.split()
        if len(args) < 2:
            return await msg.edit(
                """⛔ Cara penggunaan: `.unprem user_id/username`
Contoh:
- `.unprem 1234567890`
- `.unprem @username`
- Reply ke pesan user: `.unprem`
"""
            )
        target_id = args[1]

    try:
        target_user = await client.get_users(target_id)
    except Exception as e:
        return await msg.edit(f"❌ Error mengambil user: {e}")

    try:
        # Hapus dari PREM_USERS
        await remove_from_vars(client.me.id, "PREM_USERS", target_user.id)
        # Hapus expired date
        await rem_expired_date(target_user.id)

        return await msg.edit(f"""
**ɪɴғᴏʀᴍᴀᴛɪᴏɴ:**
<blockquote>👤 Nama: <a href="tg://user?id={target_user.id}">{target_user.first_name} {target_user.last_name or ''}</a>
🆔 ID: <code>{target_user.id}</code>
📚 Keterangan: <b>Premium Dicabut</b>
</blockquote>
""", disable_web_page_preview=True)

    except Exception as error:
        return await msg.edit(f"❌ Error: {error}")
        

@PY.UBOT("getprem")
@PY.OWNER
async def _(client, message):
    prem_users = await get_list_from_vars(client.me.id, "PREM_USERS")
    if not prem_users:
        return await message.reply_text("📭 Tidak ada pengguna premium yang ditemukan.")

    text = "<b>👑 Daftar Pengguna Premium:</b>\n\n"
    count = 0
    batch = []
    tz = timezone("Asia/Jakarta")

    # Hilangkan duplikat user
    seen = set()
    for user_id in prem_users:
        if user_id in seen:
            continue
        seen.add(user_id)

        try:
            user = await client.get_users(int(user_id))
            expired = await get_expired_date(user.id)

            if expired:
                if expired.tzinfo is None:
                    expired = tz.localize(expired)
                expired_str = expired.astimezone(tz).strftime("%d-%m-%Y %H:%M")
            else:
                expired_str = "♾️ PERMANEN"

            count += 1

            user_info = (
                f"• <b>{count}.</b> <a href='tg://user?id={user.id}'>"
                f"{user.first_name} {user.last_name or ''}</a>\n"
                f"🆔 <code>{user.id}</code>\n"
                f"⏳ Expired: <code>{expired_str}</code>\n\n"
            )

            # cek limit telegram (4096)
            if len(text) + len(user_info) > 4000:
                batch.append(text)
                text = ""

            text += user_info

        except Exception:
            continue

    if text:
        batch.append(text)

    # kirim batch satu-satu
    for idx, part in enumerate(batch):
        if idx == 0:
            # tambahin total di batch pertama
            part += f"<b>Total Premium:</b> {count} user"
        await message.reply_text(part, disable_web_page_preview=True)


@PY.UBOT("seles")
async def _(client, message):
    user = message.from_user

    # cek role
    admin_users = [int(x) for x in await get_list_from_vars(client.me.id, "ADMIN_USERS")]
    allowed_users = [OWNER_ID] + admin_users
    if user.id not in allowed_users:
        return

    msg = await message.reply("sedang memproses...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(f"<b>{message.text} user_id/username</b>")

    try:
        target = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    sudo_users = await get_list_from_vars(bot.me.id, "SELER_USERS")

    if target.id in sudo_users:
        return await msg.edit(f"""
<blockquote><b>name: [{target.first_name} {target.last_name or ''}](tg://user?id={target.id})</b>
<b>id: `{target.id}`</b>
<b>keterangan: sudah reseller</b></blockquote>
""")

    try:
        await add_to_vars(bot.me.id, "SELER_USERS", target.id)
        return await msg.edit(f"""
<blockquote><b>name: [{target.first_name} {target.last_name or ''}](tg://user?id={target.id})</b>
<b>id: `{target.id}`</b>
<b>keterangan: reseller</b></blockquote>
""")
    except Exception as error:
        return await msg.edit(error)


@PY.UBOT("unseles")
async def _(client, message):
    user = message.from_user
    if user.id != OWNER_ID:
        return
    msg = await message.reply("ꜱᴇᴅᴀɴɢ ᴍᴇᴍᴘʀᴏꜱᴇꜱ...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"<b>{message.text} ᴜsᴇʀ_ɪᴅ/ᴜsᴇʀɴᴀᴍᴇ</b>"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    seles_users = await get_list_from_vars(bot.me.id, "SELER_USERS")

    if user.id not in seles_users:
        return await msg.edit(f"""
<blockquote><b>ɴᴀᴍᴇ: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})</b>
<b>ɪᴅ: `{user.id}`</b>
<b>ᴋᴇᴛᴇʀᴀɴɢᴀɴ: ᴛɪᴅᴀᴋ ᴛᴇʀᴅᴀꜰᴛᴀʀ</ci></b></blockquote>
"""
        )

    try:
        await remove_from_vars(bot.me.id, "SELER_USERS", user.id)
        return await msg.edit(f"""
<blockquote><b>ɴᴀᴍᴇ: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})</b>
<b>ɪᴅ: `{user.id}`</b>
<b>ᴋᴇᴛᴇʀᴀɴɢᴀɴ: ᴛᴇʟᴀʜ ᴅɪ ʜᴀᴘᴜꜱ ᴅᴀʀɪ ᴅᴀᴛᴀʙᴀꜱᴇ</ci></b></blockquote>
"""
        )
    except Exception as error:
        return await msg.edit(error)


@PY.UBOT("getseles")
async def _(client, message):
    user = message.from_user
    if user.id != OWNER_ID:
        return
    Sh = await message.reply("ꜱᴇᴅᴀɴɢ ᴍᴇᴍᴘʀᴏꜱᴇꜱ...")
    seles_users = await get_list_from_vars(bot.me.id, "SELER_USERS")

    if not seles_users:
        return await Sh.edit("ᴅᴀꜰᴛᴀʀ ꜱᴇʟʟᴇʀ ᴋᴏꜱᴏɴɢ")

    seles_list = []
    for user_id in seles_users:
        try:
            user = await client.get_users(int(user_id))
            seles_list.append(
                f"<blockquote>👤 [{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) | `{user.id}`</blockquote>"
            )
        except:
            continue

    if seles_list:
        response = (
            "📋 ᴅᴀꜰᴛᴀʀ ʀᴇꜱᴇʟʟᴇʀ:\n\n"
            + "\n".join(seles_list)
            + f"\n\n• ᴛᴏᴛᴀʟ ʀᴇꜱᴇʟʟᴇʀ: {len(seles_list)}"
        )
        return await Sh.edit(response)
    else:
        return await Sh.edit("ᴛɪᴅᴀᴋ ᴅᴀᴘᴀᴛ ᴍᴇɴɢᴀᴍʙɪʟ ᴅᴀꜰᴛᴀʀ ꜱᴇʟʟᴇʀ")


@PY.UBOT("time")
async def _(client, message):
    user = message.from_user
    if user.id != OWNER_ID:
        return
    Tm = await message.reply("processing . . .")
    bajingan = message.command
    if len(bajingan) != 3:
        return await Tm.edit(f"gunakan /set_time user_id hari")
    user_id = int(bajingan[1])
    get_day = int(bajingan[2])
    print(user_id , get_day)
    try:
        get_id = (await client.get_users(user_id)).id
        user = await client.get_users(user_id)
    except Exception as error:
        return await Tm.edit(error)
    if not get_day:
        get_day = 30
    now = datetime.now(timezone("Asia/Jakarta"))
    expire_date = now + timedelta(days=int(get_day))
    await set_expired_date(user_id, expire_date)
    await Tm.edit(f"""
💬 INFORMATION
 name: {user.mention}
 id: {get_id}
 aktifkan_selama: {get_day} hari
"""
    )


@PY.UBOT("cek")
async def _(client, message):
    user = message.from_user
    if user.id != OWNER_ID:
        return
    Sh = await message.reply("ᴘʀᴏᴄᴇꜱꜱɪɴɢ . . .")
    user_id = await extract_user(message)
    if not user_id:
        return await Sh.edit("ᴘᴇɴɢɢᴜɴᴀ ᴛɪᴅᴀᴋ ᴛᴇᴍᴜᴋᴀɴ")
    try:
        get_exp = await get_expired_date(user_id)
        sh = await client.get_users(user_id)
    except Exception as error:
        return await Sh.ediit(error)
    if get_exp is None:
        await Sh.edit(f"""
<blockquote><b>ɴᴀᴍᴇ: {sh.mention}</b>
<b>ɪᴅ: `{user_id}`</b>
<b>ᴘʟᴀɴ : ɴᴏɴᴇ</b>
<b>ᴘʀᴇꜰɪx : .</b>
<b>ᴇxᴘɪʀᴇᴅ : ɴᴏɴᴀᴋᴛɪꜰ</b></blockquote>
""")
    else:
        SH = await ubot.get_prefix(user_id)
        exp = get_exp.strftime("%d-%m-%Y")
        if user_id in await get_list_from_vars(bot.me.id, "ULTRA_PREM"):
            status = "SuperUltra"
        else:
            status = "Premium"
        await Sh.edit(f"""
<blockquote><b>ɴᴀᴍᴇ: {sh.mention}</b>
<b>ɪᴅ: `{user_id}`</b>
<b>ᴘʟᴀɴ : {status}</b>
<b>ᴘʀᴇꜰɪx : {' '.join(SH)}</b>
<b>ᴇxᴘɪʀᴇᴅ : {exp}</b></blockquote>
"""
        )


@PY.UBOT("addadmin")
async def _(client, message):
    user = message.from_user
    if user.id != OWNER_ID:
        return
    msg = await message.reply("sedang memproses...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"{message.text} user_id/username"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    admin_users = await get_list_from_vars(bot.me.id, "ADMIN_USERS")

    if user.id in admin_users:
        return await msg.edit(f"""
💬 INFORMATION
name: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
id: {user.id}
keterangan: sudah dalam daftar
"""
        )

    try:
        await add_to_vars(bot.me.id, "ADMIN_USERS", user.id)
        return await msg.edit(f"""
💬 INFORMATION
name: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
id: {user.id}
keterangan: admin
"""
        )
    except Exception as error:
        return await msg.edit(error)


@PY.UBOT("unadmin")
async def _(client, message):
    user = message.from_user
    if user.id != OWNER_ID:
        return
    msg = await message.reply("sedang memproses...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"{message.text} user_id/username"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    admin_users = await get_list_from_vars(bot.me.id, "ADMIN_USERS")

    if user.id not in admin_users:
        return await msg.edit(f"""
💬 INFORMATION
name: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
id: {user.id}
keterangan: tidak daam daftar
"""
        )

    try:
        await remove_from_vars(bot.me.id, "ADMIN_USERS", user.id)
        return await msg.edit(f"""
💬 INFORMATION
name: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
id: {user.id}
keterangan: unadmin
"""
        )
    except Exception as error:
        return await msg.edit(error)


@PY.UBOT("getadmin")
async def _(client, message):
    user = message.from_user
    if user.id != OWNER_ID:
        return
    Sh = await message.reply("sedang memproses...")
    admin_users = await get_list_from_vars(bot.me.id, "ADMIN_USERS")

    if not admin_users:
        return await Sh.edit("<s>daftar admin kosong</s>")

    admin_list = []
    for user_id in admin_users:
        try:
            user = await client.get_users(int(user_id))
            admin_list.append(
                f"👤 [{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) | {user.id}"
            )
        except:
            continue

    if admin_list:
        response = (
            "📋 daftar admin:\n\n"
            + "\n".join(admin_list)
            + f"\n\n⚜️ total admin: {len(admin_list)}"
        )
        return await Sh.edit(response)
    else:
        return await Sh.edit("tidak dapat mengambil daftar admin")

@PY.UBOT("addultra")
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    user = message.from_user
    if user.id != OWNER_ID:
        return await message.reply_text(f"{ggl}mau ngapain kamu ?")
    msg = await message.reply(f"{prs}sedang memproses...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"{ggl}{message.text} user_id/username"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    ultra_users = await get_list_from_vars(bot.me.id, "ULTRA_PREM")

    if user.id in ultra_users:
        return await msg.edit(f"{ggl}sudah menjadi superultra!")

    try:
        await add_to_vars(bot.me.id, "ULTRA_PREM", user.id)
        return await msg.edit(f"{brhsl}berhasil menjadi superultra")
    except Exception as error:
        return await msg.edit(error)

@PY.UBOT("rmultra")
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    user = message.from_user
    if user.id != OWNER_ID:
        return await message.reply_text(f"{ggl}mau ngapain kamu ?")
    msg = await message.reply(f"{prs}sedang memproses...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"{ggl}{message.text} user_id/username"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    ultra_users = await get_list_from_vars(bot.me.id, "ULTRA_PREM")

    if user.id not in ultra_users:
        return await msg.edit(f"{ggl}tidak ada di dalam database superultra")

    try:
        await remove_from_vars(bot.me.id, "ULTRA_PREM", user.id)
        return await msg.edit(f"{brhsl}berhasil di hapus dari daftar superultra")
    except Exception as error:
        return await msg.edit(error)
