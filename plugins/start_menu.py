import traceback
from datetime import datetime
from telethon import events
import config
from utils import IS_OWNER
from helpers.emoji import get_premium_emoji_block
from helpers.inline import Inline

bot = config.bot

@bot.on(events.NewMessage)
async def global_debug_listener(event):
    if event.is_private and event.text:
        sender = await event.get_sender()
        name = sender.first_name if sender else "Unknown"
        print(f"📩 [CHAT MASUK] Dari: {name} (ID: {event.sender_id}) | Teks: '{event.text}'")

@bot.on(events.NewMessage(pattern=r'^/(start|settings|menu|help)(?:@\w+)?'))
async def main_menu_handler(event):
    try:
        user_id = event.sender_id
        if not IS_OWNER(user_id):
            msg_denied = (
                f"❌ <b>AKSES DITOLAK!</b>\n\n"
                f"ID Telegram Anda: <code>{user_id}</code>\n"
                f"Belum terdaftar di <code>OWNER_IDS</code>."
            )
            await event.reply(msg_denied, parse_mode="html")
            return

        if "/help" in event.text:
            await show_help(event)
        else:
            await show_dashboard(event)
    except Exception as e:
        print(f"❌ ERROR PADA HANDLER START/HELP: {e}")
        traceback.print_exc()

async def show_dashboard(event):
    now_wib = datetime.now(config.WIB).strftime('%d-%m-%Y | %H:%M:%S WIB')
    emojis = get_premium_emoji_block(4)
    text = (
        f"{emojis}\n"
        "✨ <b>PANEL BOT PESAN BERULANG (TELETHON)</b>\n"
        f"<b>Instance Bot:</b> <code>{config.BOT_NAME_TAG.upper()}</code>\n"
        f"⏳ <b>Waktu (WIB):</b> <code>{now_wib}</code>\n\n"
        "Selamat datang di Panel Kontrol Bot Pesan Berulang.\n"
        "Gunakan tombol di bawah untuk mengelola semua pesan berulang."
    )

    buttons = Inline.dashboard_menu()

    try:
        if isinstance(event, events.CallbackQuery.Event):
            await event.edit(text, buttons=buttons, parse_mode="html")
        else:
            await event.reply(text, buttons=buttons, parse_mode="html")
    except Exception as e:
        print(f"❌ GAGAL MENGIRIM PESAN BALASAN: {e}")
        traceback.print_exc()

async def show_help(event):
    emojis = get_premium_emoji_block(3)
    text = (
        f"{emojis}\n"
        "📖 <b>PANDUAN & BANTUAN BOT PESAN BERULANG</b>\n\n"
        "<blockquote>Bot ini berfungsi untuk mengirimkan pesan secara periodik/berulang otomatis ke grup atau chat target menggunakan penjadwal asinkron (APScheduler) dan zona waktu WIB.</blockquote>\n\n"
        "<b>Fitur Utama:</b>\n"
        "• ⚙️ <b>Kelola Multi-Pesan:</b> Melihat list, mengedit, atau menghapus pesan berulang.\n"
        "• ➕ <b>Buat Pesan Baru:</b> Setup wizard 5 langkah mudah.\n"
        "• ⏱️ <b>Pengulangan Fleksibel:</b> Berdasarkan menit atau jam dengan jam mulai spesifik (WIB).\n"
    )
    buttons = Inline.help_menu()
    if isinstance(event, events.CallbackQuery.Event):
        await event.edit(text, buttons=buttons, parse_mode="html")
    else:
        await event.reply(text, buttons=buttons, parse_mode="html")
