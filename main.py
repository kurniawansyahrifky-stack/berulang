import asyncio
import logging
import traceback
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import config
from database import init_db

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Mengatur AsyncIOScheduler dengan Timezone WIB
scheduler = AsyncIOScheduler(timezone=config.WIB)

async def main():
    print(f"⚡ Menginisialisasi Database Terisolasi untuk Instance: [{config.BOT_NAME_TAG}]...")
    init_db()

    print("📦 Dynamic Loading Plugins...")
    import plugins

    print(f"🚀 Menghubungkan Bot Telethon [{config.BOT_NAME_TAG}]...")
    await config.bot.start(bot_token=config.BOT_TOKEN)
    
    me = await config.bot.get_me()
    print(f"\n==========================================")
    print(f"✅ BOT AKTIF! Logged in as: @{me.username} (ID: {me.id}) [Tag: {config.BOT_NAME_TAG}]")
    print(f"==========================================\n")

    scheduler.start()
    await config.bot.run_until_disconnected()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print("\n❌ TERJADI ERROR PADA BOT:")
        traceback.print_exc()
