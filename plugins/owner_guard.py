from telethon import events
import config
from helpers.emoji import get_premium_emoji_block

bot = config.bot

@bot.on(events.ChatAction)
async def auto_leave_unauthorized_groups(event):
    if event.is_group or event.is_channel:
        me = await bot.get_me()
        if event.user_added and event.user_id == me.id:
            if event.added_by_id not in config.OWNER_IDS:
                emojis = get_premium_emoji_block(2)
                msg = (
                    f"{emojis}\n"
                    '<tg-emoji emoji-id="6138508581047111774">❌</tg-emoji> <b>AKSES DITOLAK!</b>\n\n'
                    "<blockquote>Bot Pesan Berulang ini khusus dipasang oleh OWNER!</blockquote>"
                )
                await event.respond(msg, parse_mode="html")
                await bot.leave_chat(event.chat_id)
