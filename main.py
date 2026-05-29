import os
os.makedirs("/app/sessions", exist_ok=True)

from telethon import TelegramClient, events
from telethon.tl.types import User
import asyncio
from datetime import datetime

api_id = 39262064
api_hash = "64e003980dddfb0bfc6bbd4ea9e717bb"
session_name = "/app/sessions/ardosher_session"

client = TelegramClient(session_name, api_id, api_hash)

replied_users = set()

AUTO_REPLY_MESSAGE = (
    "Salom! Hozir band yoki uxlayapman. "
    "Xabaringizni o'qib, tez orada javob beraman. 🙏"
)


@client.on(events.NewMessage(incoming=True))
async def handle_message(event):
    """Faqat shaxsiy xabarlarga, faqat haqiqiy foydalanuvchilarga,
    faqat soat 00:00-10:00 oraligida bir marta javob berish."""
    # Faqat shaxsiy (private) suhbatlar
    if not event.is_private:
        return

    sender = await event.get_sender()

    # Faqat haqiqiy foydalanuvchilar (botlar emas)
    if not isinstance(sender, User) or sender.bot:
        return

    now = datetime.now()
    if not (0 <= now.hour < 10):
        return

    if sender.id in replied_users:
        return

    replied_users.add(sender.id)
    await event.reply(AUTO_REPLY_MESSAGE)
    print(f"Javob yuborildi: {sender.first_name} (id={sender.id})")


async def keep_online():
    """Har 60 soniyada typing holati korsatib akkauntni online saqlaydi."""
    while True:
        try:
            me = await client.get_me()
            async with client.action(me, "typing"):
                await asyncio.sleep(2)
        except Exception as e:
            print(f"keep_online xatosi: {e}")
        await asyncio.sleep(60)


async def main():
    # Avval ulanish, keyin avtorizatsiyani tekshirish
    await client.start()

    me = await client.get_me()
    print(f"Akkaunt ulandi: {me.first_name}")
    print("================================")
    print("24/7 online ishlayapti...")
    print("================================")

    asyncio.ensure_future(keep_online())

    await client.run_until_disconnected()


with client:
    client.loop.run_until_complete(main())
