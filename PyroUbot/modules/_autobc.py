import asyncio
import random
from datetime import datetime, timedelta
from pyrogram.enums import ChatType
from pyrogram.errors import FloodWait
from PyroUbot import *

AG = {}  # per userbot id: {"status": bool, "round": int, "last": datetime, "next": datetime}
BLACKLIST_CHAT = []  # default kosong, tambahin ID grup kalau mau exclude


def now_wib():
    return datetime.utcnow() + timedelta(hours=7)  # UTC+7


def fmt_wib(dt: datetime | None):
    if not dt:
        return "-"
    return dt.strftime("%Y-%m-%d %H:%M:%S WIB")


def parse_autobc_args(message):
    text = (message.text or message.caption or "").strip()
    parts = text.split()
    if len(parts) < 2:
        return ("help", "")
    cmd = parts[1].lower()
    val = parts[2] if len(parts) > 2 else ""
    return (cmd, val)


# ======================
# Core AutoBC
# ======================
async def run_autobc(client):
    AG[client.me.id] = {
        "status": True,
        "round": AG.get(client.me.id, {}).get("round", 0),
        "last": AG.get(client.me.id, {}).get("last"),
        "next": AG.get(client.me.id, {}).get("next"),
    }

    while AG[client.me.id]["status"]:
        delay_minutes = int(await get_vars(client.me.id, "DELAY_GCAST") or 60)
        per_group_delay = int(await get_vars(client.me.id, "PER_GROUP_DELAY") or 3)

        blacklist = await get_list_from_vars(client.me.id, "BL_ID")
        auto_texts = await get_auto_text(client.me.id)

        if not auto_texts:
            await client.send_message(client.me.id, "<b><i>💤 Tidak ada pesan yang disimpan.</i></b>")
            AG[client.me.id]["status"] = False
            await set_vars(client.me.id, "AUTOBCAST", "off")
            return

        message_to_forward = random.choice(auto_texts)
        group_success, failed = 0, 0
        AG[client.me.id]["round"] = AG[client.me.id].get("round", 0) + 1
        total_round = AG[client.me.id]["round"]

        async for dialog in client.get_dialogs():
            if not AG[client.me.id]["status"]:
                await client.send_message(client.me.id, "<b><i>⛔️ Auto Broadcast dihentikan.</i></b>")
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
                except Exception:
                    failed += 1
                await asyncio.sleep(per_group_delay)

        next_run = now_wib() + timedelta(minutes=delay_minutes)
        AG[client.me.id]["last"] = now_wib()
        AG[client.me.id]["next"] = next_run

        await client.send_message(
            client.me.id,
            f"""
<b>⚡️ AutoBC Putaran Selesai</b>
✅ Berhasil : {group_success} Chat
❌ Gagal : {failed} Chat
⏳ Putaran Ke : {total_round}
🕒 Jeda Putaran : {delay_minutes} Menit
⏱️ Delay per Grup : {per_group_delay} Detik
📆 Next AutoBC : <b>{fmt_wib(next_run)}</b>
"""
        )

        await asyncio.sleep(60 * delay_minutes)


# ======================
# Commands
# ======================
@PY.UBOT("autobc")
async def _(client, message):
    msg = await message.reply("<b><i>⚡ Processing...</i></b>")
    cmd, value = parse_autobc_args(message)

    if cmd == "on":
        if AG.get(client.me.id, {}).get("status"):
            return await msg.edit("<b><i>⚡ Auto Broadcast sudah aktif.</i></b>")
        if not await get_vars(client.me.id, "DELAY_GCAST"):
            await set_vars(client.me.id, "DELAY_GCAST", "60")
        if not await get_vars(client.me.id, "PER_GROUP_DELAY"):
            await set_vars(client.me.id, "PER_GROUP_DELAY", "3")
        await set_vars(client.me.id, "AUTOBCAST", "on")
        await msg.edit("<b><i>⚡ Auto Broadcast diaktifkan.</i></b>")
        asyncio.create_task(run_autobc(client))

    elif cmd == "off":
        AG[client.me.id] = {"status": False, "round": AG.get(client.me.id, {}).get("round", 0)}
        await set_vars(client.me.id, "AUTOBCAST", "off")
        return await msg.edit("<b><i>⛔ Auto Broadcast dihentikan.</i></b>")

    elif cmd == "status":
        status = "✅ Enabled" if AG.get(client.me.id, {}).get("status") else "⛔ Disabled"
        delay_minutes = int(await get_vars(client.me.id, "DELAY_GCAST") or 60)
        per_group_delay = int(await get_vars(client.me.id, "PER_GROUP_DELAY") or 3)
        auto_texts = await get_auto_text(client.me.id)
        total_round = AG.get(client.me.id, {}).get("round", 0)
        last_bc = fmt_wib(AG.get(client.me.id, {}).get("last"))
        next_bc = fmt_wib(AG.get(client.me.id, {}).get("next"))

        teks = f"""
📎 <b>Auto Broadcast Status</b>:

<details><summary>📊 Klik untuk lihat status</summary>

👤 Status: {status}
🏓 Pause Rotation: {delay_minutes} Min
✉️ Save Messages: {len(auto_texts) if auto_texts else 0}
⚙️ Total Rounds: {total_round} Times
⏰ Last Broadcast: {last_bc}
⚡️ Next Broadcast: {next_bc}

</details>
"""
        return await msg.edit(teks, disable_web_page_preview=True)

    elif cmd == "delay":
        if not value.isdigit():
            return await msg.edit("<b><i>⛔ Format salah! Gunakan <code>.autobc delay [menit]</code></i></b>")
        await set_vars(client.me.id, "DELAY_GCAST", value)
        return await msg.edit(f"<b><i>😐 Delay antar putaran diatur ke {value} menit.</i></b>")

    elif cmd == "perdelay":
        if not value.isdigit():
            return await msg.edit("<b><i>⛔ Format salah! Gunakan <code>.autobc perdelay [detik]</code></i></b>")
        val = int(value)
        if val < 3:
            return await msg.edit("<b><i>⛔ Minimal delay per grup adalah 3 detik.</i></b>")
        await set_vars(client.me.id, "PER_GROUP_DELAY", str(val))
        return await msg.edit(f"<b><i>😐 Delay per grup diatur ke {val} detik.</i></b>")

    elif cmd == "save":
        if not message.reply_to_message:
            return await msg.edit("<b><i>⛔ Harap reply ke pesan yang ingin disimpan.</i></b>")

        # Forward pesan ke "Saved Messages"
        saved_msg = await message.reply_to_message.forward("me")

        # ✅ Overwrite (hanya simpan 1 pesan, tidak bisa dobel)
        await set_vars(client.me.id, "AUTO_TEXTS", f"[{saved_msg.id}]")

        return await msg.edit(
            f"<b><i>✅ Pesan baru disimpan dengan ID <code>{saved_msg.id}</code> "
            f"(pesan lama dihapus, hanya 1 tersisa)</i></b>"
        )

    elif cmd == "list":
        auto_texts = await get_auto_text(client.me.id)
        if not auto_texts:
            return await msg.edit("<b><i>💤 Tidak ada pesan tersimpan.</i></b>")
        teks = "\n".join([f"{i+1}. ID: <code>{t}</code>" for i, t in enumerate(auto_texts)])
        return await msg.edit(f"<b><i>⚡️ Daftar Pesan AutoBC:</i></b>\n\n{teks}")

    elif cmd == "remove":
        if not value.isdigit():
            return await msg.edit("<b><i>⛔ Harap masukkan nomor urut yang valid.</i></b>")
        idx = int(value) - 1
        auto_texts = await get_auto_text(client.me.id)
        if not auto_texts:
            return await msg.edit("<b><i>💤 Tidak ada pesan tersimpan.</i></b>")
        if idx < 0 or idx >= len(auto_texts):
            return await msg.edit("<b><i>⛔ Nomor urut tidak ditemukan.</i></b>")
        removed = auto_texts[idx]
        await remove_auto_text(client.me.id, idx)
        return await msg.edit(f"<b><i>⚙️ Pesan dengan ID <code>{removed}</code> berhasil dihapus.</i></b>")

    else:
        return await msg.edit("<b><i>⛔ Format salah! Gunakan .autobc [query] - [value]</i></b>")


# ======================
# Auto Resume on start
# ======================
async def resume_autobc(client):
    status = await get_vars(client.me.id, "AUTOBCAST")
    if status == "on":
        delay_minutes = int(await get_vars(client.me.id, "DELAY_GCAST") or 60)
        per_group_delay = int(await get_vars(client.me.id, "PER_GROUP_DELAY") or 3)
        round_no = AG.get(client.me.id, {}).get("round", 0) + 1

        next_run = now_wib() + timedelta(minutes=delay_minutes)
        AG[client.me.id] = {
            "status": True,
            "round": round_no,
            "last": None,
            "next": next_run,
        }

        await client.send_message(
            client.me.id,
            f"""📣 AutoBC #{round_no} (Resume)
🕒 Delay antar putaran: {delay_minutes} menit
⏱️ Delay per grup: {per_group_delay} detik
📆 Next AutoBC : <b>{fmt_wib(next_run)}</b>
"""
        )
        asyncio.create_task(run_autobc(client))


@PY.UBOT("start")
async def start_handler(client, message):
    await resume_autobc(client)
    return await message.reply("✅ Bot sudah berjalan.")
