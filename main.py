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

# Allaqachon javob berilgan foydalanuvchilarni kuzatish
replied_users = set()

AUTO_REPLY_MESSAGE = (
    "Salom! Hozir band bo'lganimiz sababli xabaringizga javob bera olmayapmiz. "
    "Tez orada siz bilan bog'lanamiz. Rahmat! 🙏"
)

@client.on(events.NewMessage(incoming=True))
async def handle_message(event):
    """Faqat shaxsiy xabarlarga avtomatik javob berish (0-10 soat oralig'ida)"""
    # Faqat shaxsiy (private) xabarlarga javob berish
    if not event.is_private:
        return

    sender = await event.get_sender()

    # Foydalanuvchi ekanligini tekshirish (bot yoki kanal emas)
    if not isinstance(sender, User) or sender.bot:
        return

    sender_id = sender.id
    current_hour = datetime.now().hour

    print(f"📨 {sender.first_name} (ID: {sender_id}): {event.message.message}")

    # Faqat 0-10 soat oralig'ida va bir marta javob berish
    if current_hour < 10 and sender_id not in replied_users:
        await event.reply(AUTO_REPLY_MESSAGE)
        replied_users.add(sender_id)
        print(f"✅ Avtomatik javob yuborildi: {sender.first_name}")
    else:
        if sender_id in replied_users:
            print(f"⏭️ {sender.first_name} ga avval javob berilgan, o'tkazib yuborildi.")
        else:
            print(f"⏰ Soat {current_hour}:00 — avtomatik javob vaqti emas (0-10 soat).")


async def keep_online():
    """Akkauntni faol ushlab turish uchun yozish indikatorini simulyatsiya qilish"""
    while True:
        try:
            me = await client.get_me()
            # O'ziga yozish indikatorini yuborish (hech kimga ko'rinmaydi)
            async with client.action(me.id, "typing"):
                await asyncio.sleep(3)
        except Exception as e:
            print(f"⚠️ keep_online xatosi: {e}")
        await asyncio.sleep(60)


async def main():
    await client.start()

    me = await client.get_me()
    print(f"✅ Akkaunt ulandi: {me.first_name}")
    print("================================")
    print("24/7 online ishlayapti...")
    print("================================")

    # Akkauntni faol ushlab turuvchi vazifani fonda ishga tushirish
    asyncio.create_task(keep_online())

    await client.run_until_disconnected()


if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
