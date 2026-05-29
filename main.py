from telethon import TelegramClient, events
import asyncio
from datetime import datetime

# =====================================
# API MA'LUMOTLARI
# =====================================

api_id = 39262064
api_hash = "64e003980dddfb0bfc6bbd4ea9e717bb"

# Session nomi
session_name = "ardosher_session"

# =====================================
# CLIENT
# =====================================

client = TelegramClient(session_name, api_id, api_hash)

# =====================================
# AUTO JAVOB
# =====================================

AUTO_REPLY = """
Assalomu alaykum 😊

Hozir online emasman.
Keyinroq javob yozib yuboraman.
"""

# Javob berilgan userlar
replied_users = set()

# =====================================
# XABAR KELGANDA
# =====================================


@client.on(events.NewMessage(incoming=True))
async def handler(event):
    try:
        # Faqat private chat
        if not event.is_private:
            return

        sender_id = event.sender_id

        # Hozirgi vaqt
        now = datetime.now()
        hour = now.hour

        # 00:00 dan 10:00 gacha
        if 0 <= hour < 10:

            # Bir userga bir marta javob
            if sender_id not in replied_users:

                await event.reply(AUTO_REPLY)

                replied_users.add(sender_id)

                print(f"Auto reply yuborildi: {sender_id}")

    except Exception as e:
        print("Xatolik:", e)


# =====================================
# ONLINE USHLAB TURISH
# =====================================


async def keep_online():
    while True:
        try:
            me = await client.get_me()

            # O'ziga typing yuboradi
            async with client.action(me.id, "typing"):
                await asyncio.sleep(4)

            print("Akkaunt online ishlayapti...")

            # Har 30 sekund
            await asyncio.sleep(30)

        except Exception as e:
            print("Online xatolik:", e)
            await asyncio.sleep(10)


# =====================================
# MAIN
# =====================================


async def main():
    await client.start()

    me = await client.get_me()

    print("================================")
    print(f"Akkaunt ulandi: {me.first_name}")
    print("24/7 online ishlayapti...")
    print("================================")

    # Online task
    asyncio.create_task(keep_online())

    # Bot ishlashi
    await client.run_until_disconnected()


# =====================================
# START
# =====================================

with client:
    client.loop.run_until_complete(main())
