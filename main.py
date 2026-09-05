import asyncio
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

API_ID = 36076557
API_HASH = "02ec3d65721fa6aee4c1c4a93bc14660"
BOT_TOKEN = "8696254716:AAE5MhZO_PX0GTEJQrmaeH6xg94JDnDRdFA"

bot = TelegramClient("auto_cleaner_bot", API_ID, API_HASH)


@bot.on(events.NewMessage(pattern="/temizle"))
async def clean_chat(event):
    try:
        participants = await bot.get_participants(event.chat_id)

        for user in participants:
            if user.is_self:
                continue

            try:
                await bot(
                    EditBannedRequest(
                        event.chat_id,
                        user.id,
                        ChatBannedRights(until_date=None, view_messages=True),
                    )
                )
                await asyncio.sleep(0.5)

            except FloodWaitError as e:
                await asyncio.sleep(e.seconds)
            except Exception:
                pass

        await event.respond("Tamamlandı.")

    except Exception as e:
        await event.respond(f"Hata: {e}")


print("Bot başlatılıyor...")
bot.start(bot_token=BOT_TOKEN)
print("Bot çalışıyor!")
bot.run_until_disconnected()
