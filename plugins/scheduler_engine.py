import json
import os
from datetime import datetime
from telethon import events, types
import config
from main import scheduler
from database import get_db
from utils import IS_OWNER, parse_custom_buttons
from helpers.emoji import get_premium_emoji_block
from helpers.inline import Inline

bot = config.bot
user_fsm = {}

async def execute_periodic_job(task_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT chat_id, msg_text, photo_path, buttons_json, last_msg_id FROM periodic_tasks WHERE id=? AND status='RUNNING'", (task_id,))
    task = c.fetchone()

    if not task:
        conn.close()
        return

    chat_id, msg_text, photo_path, buttons_json, last_msg_id = task

    tele_buttons = []
    if buttons_json:
        parsed_rows = json.loads(buttons_json)
        for row in parsed_rows:
            btn_row = []
            for b in row:
                style_map = {
                    "primary": types.KeyboardButtonStyle(bg_primary=True),
                    "success": types.KeyboardButtonStyle(bg_success=True),
                    "danger": types.KeyboardButtonStyle(bg_danger=True)
                }
                btn_style = style_map.get(b.get("style"), types.KeyboardButtonStyle(bg_primary=True))
                btn_row.append(types.KeyboardButtonUrl(text=b['text'], url=b['url'], style=btn_style))
            tele_buttons.append(btn_row)

    if last_msg_id:
        try:
            await bot.delete_messages(chat_id, last_msg_id)
        except:
            pass

    try:
        if photo_path and os.path.exists(photo_path):
            sent = await bot.send_file(chat_id, photo_path, caption=msg_text or "", buttons=tele_buttons or None, parse_mode="html")
        else:
            sent = await bot.send_message(chat_id, msg_text, buttons=tele_buttons or None, parse_mode="html")

        if sent:
            c.execute("UPDATE periodic_tasks SET last_msg_id=? WHERE id=?", (sent.id, task_id))
            conn.commit()
    except Exception as e:
        print(f"❌ Error Job ID #{task_id}: {e}")
    finally:
        conn.close()

@bot.on(events.CallbackQuery)
async def scheduler_callback(event):
    data = event.data.decode('utf-8')
    user_id = event.sender_id

    if not IS_OWNER(user_id):
        return await event.answer("❌ Akses Khusus Owner!", alert=True)

    if data == "manage_tasks":
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT id, title, interval_val, interval_type, start_hour FROM periodic_tasks")
        tasks = c.fetchall()
        conn.close()

        emojis = get_premium_emoji_block(2)
        text = f"{emojis}\n🚀 <b>DAFTAR PESAN BERULANG AKTIF:</b>\n\n"
        if tasks:
            for t in tasks:
                text += f"• <b>{t['title']}</b> (ID #{t['id']}) - Tiap {t['interval_val']} {t['interval_type']} (Jam {t['start_hour']:02d}:00 WIB)\n"
        else:
            text += "<i>Belum ada pesan berulang yang dibuat.</i>\n"

        buttons = Inline.task_list_menu(tasks)
        await event.edit(text, buttons=buttons, parse_mode="html")

    elif data == "menu_main":
        user_fsm.pop(user_id, None)
        from plugins.start_menu import show_dashboard
        await show_dashboard(event)

    elif data == "help_menu":
        from plugins.start_menu import show_help
        await show_help(event)

    elif data == "close_panel":
        await event.delete()

    elif data == "create_task":
        user_fsm[user_id] = {'step': 'TITLE', 'chat_id': event.chat_id}
        buttons = Inline.cancel_menu(b"manage_tasks")
        await event.edit(
            "📝 <b>LANGKAH 1: Masukkan Judul Pesan</b>\n"
            "Contoh: <code>Pesan 1 - Promosi</code> atau <code>Pesan 2 - Rules</code>",
            buttons=buttons,
            parse_mode="html"
        )

    elif data.startswith("del_task_"):
        tid = int(data.split("_")[2])
        conn = get_db()
        c = conn.cursor()
        c.execute("DELETE FROM periodic_tasks WHERE id=?", (tid,))
        conn.commit()
        conn.close()

        try:
            scheduler.remove_job(f"task_{tid}")
        except:
            pass

        await event.answer(f"✅ Pesan #{tid} Dihapus!", alert=True)
        event.data = b"manage_tasks"
        await scheduler_callback(event)

    elif data.startswith("hour_"):
        shour = int(data.split("_")[1])
        user_fsm[user_id]['start_hour'] = shour
        
        buttons = Inline.interval_menu()
        await event.edit("⏰ <b>LANGKAH 5: Pilih Durasi Pengulangan Pesan</b>", buttons=buttons, parse_mode="html")

    elif data.startswith("inter_"):
        parts = data.split("_")
        itype = "minute" if parts[1] == 'm' else "hour"
        ival = int(parts[2])

        state = user_fsm[user_id]
        
        conn = get_db()
        c = conn.cursor()
        c.execute('''INSERT INTO periodic_tasks (title, chat_id, msg_text, photo_path, buttons_json, start_hour, interval_type, interval_val)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (
            state['title'], state['chat_id'], state['text'], state.get('photo_path'),
            state.get('buttons_json'), state['start_hour'], itype, ival
        ))
        task_id = c.lastrowid
        conn.commit()
        conn.close()

        # Menjadwalkan dengan scheduler (menggunakan WIB lewat apscheduler)
        if itype == 'minute':
            scheduler.add_job(execute_periodic_job, 'interval', minutes=ival, args=[task_id], id=f"task_{task_id}", timezone=config.WIB)
        else:
            scheduler.add_job(execute_periodic_job, 'interval', hours=ival, args=[task_id], id=f"task_{task_id}", timezone=config.WIB)

        if not scheduler.running:
            scheduler.start()

        user_fsm.pop(user_id, None)
        await event.edit(
            f"✅ <b>PESAN [{state['title']}] (ID #{task_id}) BERHASIL DISIMPAN & DIJALANKAN!</b>",
            buttons=[[types.KeyboardButtonCallback(text="🔙 Kembali ke List", data=b"manage_tasks", style=types.KeyboardButtonStyle(bg_primary=True))]],
            parse_mode="html"
        )

@bot.on(events.NewMessage)
async def input_fsm_handler(event):
    user_id = event.sender_id
    if user_id not in user_fsm or event.text.startswith('/'):
        return

    state = user_fsm[user_id]
    step = state.get('step')

    if step == 'TITLE':
        state['title'] = event.text
        state['step'] = 'TEXT'
        await event.respond("🔹 <b>LANGKAH 2: Kirim Teks Pesan Berulang</b>", parse_mode="html")

    elif step == 'TEXT':
        state['text'] = event.text
        state['step'] = 'BUTTONS'
        await event.respond(
            "🔘 <b>LANGKAH 3: Masukkan Custom Buttons</b>\n\n"
            "Format:\n"
            "<code>Tombol 1 - https://link1.com | Tombol 2 - https://link2.com [danger]</code>\n\n"
            "<i>Ketik <b>skip</b> jika tanpa tombol.</i>",
            parse_mode="html"
        )

    elif step == 'BUTTONS':
        if event.text.lower() != 'skip':
            state['buttons_json'] = parse_custom_buttons(event.text)
        else:
            state['buttons_json'] = None

        state['step'] = 'HOUR'
        buttons = Inline.hours_menu()
        await event.respond("⏰ <b>LANGKAH 4: Pilih Jam Mulai Pengiriman (WIB)</b>", buttons=buttons, parse_mode="html")
