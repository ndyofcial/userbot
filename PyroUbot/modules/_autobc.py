import asyncio
import random
from datetime import datetime, timedelta
from pyrogram.enums import ChatType
from pyrogram.errors import FloodWait
from PyroUbot import *

# ======================
# State AutoBC
# ======================
AG = {}  # per userbot id: {"status": bool, "round": int}

# ======================
# Emoji helper (optional)
# ======================
def emoji(alias):
    emojis = {
        "PROCES": "<emoji id=5080331039922980916>⚡️</emoji>",
        "AKTIF": "<emoji id=5080331039922980916>⚡️</emoji>",
        "SAKTIF": "<emoji id=5080331039922980916>⚡️</emoji>",
        "TTERSIMPAN": "<emoji id=4904714384149840580>💤</emoji>",
        "STOPB": "<emoji id=4918014360267260850>⛔️</emoji>",
        "SUCSESB": "<emoji id=5355051922862653659>🤖</emoji>",
        "BERHASIL": "<emoji id=5372917041193828849>🚀</emoji>",
        "GAGALA": "<emoji id=5332296662142434561>⛔️</emoji>",
        "DELAYY": "<emoji id=5438274168422409988>😐</emoji>",
        "BERHASILS": "<emoji id=5123293121043497777>✅</emoji>",
        "DELETES": "<emoji id=5902432207519093015>⚙️</emoji>",
        "STARS": "<emoji id=5080331039922980916>⚡️</emoji>",
        "PREM": "<emoji id=5893034681636491040>📱</emoji>",
        "PUTAR": "<emoji id=5372849966689566579>✈️</emoji>",
    }
    return emojis.get(alias, "🕸")

prcs   = emoji("PROCES")
aktf   = emoji("AKTIF")
saktf  = emoji("SAKTIF")
ttsmp  = emoji("TTERSIMPAN")
stopb  = emoji("STOPB")
scsb   = emoji("SUCSESB")
brhsl  = emoji("BERHASIL")
ggla   = emoji("GAGALA")
delayy = emoji("DELAYY")
brhsls = emoji("BERHASILS")
dlts   = emoji("DELETES")
stars  = emoji("STARS")
prem   = emoji("PREM")
put    = emoji("PUTAR")

# ======================
# Utils
# ======================
def now_wib():
    # WIB = UTC+7 tanpa ketergantungan zoneinfo
    return datetime.utcnow() + timedelta(hours=7)

def fmt_wib(dt: datetime):
    # dd-mm-yy HH:MM:SS (sesuai permintaan “16-26-23” = dd-mm-yy)
    return dt.strftime("%d-%m-%y %H:%M:%S")

def parse_autobc_args(message):
    """
    Parsir perintah .autobc
    Bentuk yang didukung:
      .autobc on
      .autobc off
      .autobc delay 60
      .autobc perdelay 3
      .autobc text  (reply ke pesan)
      .autobc list
      .autobc remove 2
    """
    text = (message.text or message.caption or "").strip()
    parts = text.split()
    # parts[0] = .autobc (atau prefix lain), parts[1:] = argumen
    if len(parts) < 2:
        return ("help", "")
    cmd = parts[1].lower()
    val = parts[2] if len(parts) > 2 else ""
    return (cmd, val)

# ======================
# Core AutoBC
# ======================
async def run_autobc(client):
    """Loop utama AutoBC"""
    AG[client.me.id] = {"status": True, "round": AG.get(client.me.id, {}).get("round", 0)}

    while AG[client.me.id]["status"]:
        delay_minutes = int(await get_vars(client.me.id, "DELAY_GCAST") or 60)  # menit antar putaran
        per_group_delay = int(await get_vars(client.me.id, "PER_GROUP_DELAY") or 3)  # detik antar grup

        blacklist = await get_list_from_vars(client.me.id, "BL_ID")
        auto_texts = await get_auto_text(client.me.id)

        if not auto_texts:
            await client.send_message(client.me.id, f"<b><i>{ttsmp} Tidak ada pesan yang disimpan.</i></b>")
            AG[client.me.id]["status"] = False
            await set_vars(client.me.id, "AUTOBCAST", "off")
            return

        # pilih 1 pesan acak dari daftar ID tersimpan (disimpan di Saved Messages)
        message_to_forward = random.choice(auto_texts)
        group_success, failed = 0, 0
        AG[client.me.id]["round"] = AG[client.me.id].get("round", 0) + 1
        total_round = AG[client.me.id]["round"]

        async for dialog in client.get_dialogs():
            if not AG[client.me.id]["status"]:
                await client.send_message(client.me.id, f"<b><i>{stopb} Auto Broadcast dihentikan.</i></b>")
                return

            if (
                dialog.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP)
                and dialog.chat.id not in blacklist
                and dialog.chat.id not in BLACKLIST_CHAT
            ):
                try:
                    await client.forward_messages(dialog.chat.id, "me", message_to_forward)
                    group_success += 1
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                except Exception as err:
                    failed += 1
                    # log error forward
                    await client.send_message(client.me.id, f"❌ Gagal forward ke {dialog.chat.id}\nError: {err}")

                await asyncio.sleep(per_group_delay)  # jeda antar grup biar aman

        # Hitung jadwal berikutnya (WIB)
        next_run = now_wib() + timedelta(minutes=delay_minutes)
        next_str = fmt_wib(next_run)

        await client.send_message(
            client.me.id,
            f"""
<b>⚡️ AutoBC Putaran Selesai</b>
✅ Berhasil : {group_success} Chat
❌ Gagal : {failed} Chat
⏳ Putaran Ke : {total_round}
🕒 Jeda Putaran : {delay_minutes} Menit
⏱️ Delay per Grup : {per_group_delay} Detik
📆 Next AutoBC (WIB) : <b>{next_str}</b>
"""
        )

        await asyncio.sleep(60 * delay_minutes)

# ======================
# Commands
# ======================
@PY.UBOT("autobc")
async def _(client, message):
    msg = await message.reply(f"<b><i>{prcs} Processing...</i></b>")
    cmd, value = parse_autobc_args(message)

    if cmd == "on":
        if AG.get(client.me.id, {}).get("status"):
            return await msg.edit(f"<b><i>{saktf} Auto Broadcast sudah aktif.</i></b>")

        # set default delay kalau belum ada
        if not await get_vars(client.me.id, "DELAY_GCAST"):
            await set_vars(client.me.id, "DELAY_GCAST", "60")
        if not await get_vars(client.me.id, "PER_GROUP_DELAY"):
            await set_vars(client.me.id, "PER_GROUP_DELAY", "3")

        await set_vars(client.me.id, "AUTOBCAST", "on")
        await msg.edit(f"<b><i>{aktf} Auto Broadcast diaktifkan.</i></b>")
        asyncio.create_task(run_autobc(client))

    elif cmd == "off":
        AG[client.me.id] = {"status": False, "round": AG.get(client.me.id, {}).get("round", 0)}
        await set_vars(client.me.id, "AUTOBCAST", "off")
        return await msg.edit(f"<b><i>{stopb} Auto Broadcast dihentikan.</i></b>")

    elif cmd == "delay":
        if not value.isdigit():
            return await msg.edit(f"<b><i>{stopb} Format salah! Gunakan <code>.autobc delay [menit]</code></i></b>")
        await set_vars(client.me.id, "DELAY_GCAST", value)
        return await msg.edit(f"<b><i>{delayy} Delay antar putaran diatur ke {value} menit.</i></b>")

    elif cmd == "perdelay":
        if not value.isdigit():
            return await msg.edit(f"<b><i>{stopb} Format salah! Gunakan <code>.autobc perdelay [detik]</code></i></b>")
        val = int(value)
        if val < 3:  # minimal 3 detik biar aman
            return await msg.edit(f"<b><i>{stopb} Minimal delay per grup adalah 3 detik.</i></b>")
        await set_vars(client.me.id, "PER_GROUP_DELAY", str(val))
        return await msg.edit(f"<b><i>{delayy} Delay per grup diatur ke {val} detik.</i></b>")

    elif cmd == "text":
        if not message.reply_to_message:
            return await msg.edit(f"<b><i>{stopb} Harap reply ke pesan yang ingin disimpan.</i></b>")
        saved_msg = await message.reply_to_message.copy("me")
        await add_auto_text(client.me.id, saved_msg.id)
        return await msg.edit(f"<b><i>{brhsls} Pesan berhasil disimpan dengan ID <code>{saved_msg.id}</code></i></b>")

    elif cmd == "list":
        auto_texts = await get_auto_text(client.me.id)
        if not auto_texts:
            return await msg.edit(f"<b><i>{ttsmp} Tidak ada pesan tersimpan.</i></b>")
        teks = "\n".join([f"{i+1}. ID: <code>{t}</code>" for i, t in enumerate(auto_texts)])
        return await msg.edit(f"<b><i>{stars} Daftar Pesan AutoBC:</i></b>\n\n{teks}")

    elif cmd == "remove":
        if not value.isdigit():
            return await msg.edit(f"<b><i>{stopb} Harap masukkan nomor urut yang valid. Contoh: <code>.autobc remove 2</code></i></b>")
        idx = int(value) - 1
        auto_texts = await get_auto_text(client.me.id)
        if not auto_texts:
            return await msg.edit(f"<b><i>{ttsmp} Tidak ada pesan tersimpan.</i></b>")
        if idx < 0 or idx >= len(auto_texts):
            return await msg.edit(f"<b><i>{stopb} Nomor urut tidak ditemukan.</i></b>")
        removed = auto_texts[idx]
        await remove_auto_text(client.me.id, idx)
        return await msg.edit(f"<b><i>{dlts} Pesan dengan ID <code>{removed}</code> berhasil dihapus.</i></b>")

    else:
        return await msg.edit(
            f"""<b>📣 AutoBC Help</b>

<code>.autobc on</code> — aktifkan
<code>.autobc off</code> — hentikan
<code>.autobc delay 60</code> — jeda antar putaran (menit)
<code>.autobc perdelay 3</code> — jeda antar grup (detik, min 3)
<code>.autobc text</code> — reply ke pesan untuk disimpan
<code>.autobc list</code> — daftar pesan tersimpan
<code>.autobc remove 2</code> — hapus pesan tersimpan nomor 2
"""
        )

# ======================
# Auto Resume on start
# ======================
async def resume_autobc(client):
    """Dipanggil otomatis pas start ubot"""
    status = await get_vars(client.me.id, "AUTOBCAST")
    if status == "on":
        delay_minutes = int(await get_vars(client.me.id, "DELAY_GCAST") or 60)
        per_group_delay = int(await get_vars(client.me.id, "PER_GROUP_DELAY") or 3)
        round_no = AG.get(client.me.id, {}).get("round", 0) + 1

        next_run = now_wib() + timedelta(minutes=delay_minutes)
        next_str = fmt_wib(next_run)

        await client.send_message(
            client.me.id,
            f"""📣 AutoBC #{round_no} (Resume)
🕒 Delay antar putaran: {delay_minutes} menit
⏱️ Delay per grup: {per_group_delay} detik
📆 Next AutoBC (WIB) : <b>{next_str}</b>
"""
        )
        asyncio.create_task(run_autobc(client))

@PY.UBOT("start")
async def start_handler(client, message):
    await resume_autobc(client)
    return await message.reply("✅ Bot sudah berjalan.")
