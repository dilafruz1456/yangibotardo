import os
os.makedirs("/app/sessions", exist_ok=True)

from telethon import TelegramClient, events
import asyncio
from datetime import datetime

api_id = 39262064
api_hash = "64e003980dddfb0bfc6bbd4ea9e717bb"
session_name = "/app/sessions/ardosher_session"

client = TelegramClient(session_name, api_id, api_hash)

@client.on(events.NewMessage(incoming=True))
async def handle_message(event):
    """Har bir xabar uchun javob berish"""
    sender = await event.get_sender()
    message_text = event.message.message
    
    print(f"📨 {sender.first_name}: {message_text}")
    
    # Javob berish
    await event.reply(f"✅ Xabar qabul qilindi: {message_text}")

async def main():
    # Login qilish
    if not await client.is_user_authorized():
        await client.start()
    
    me = await client.get_me()
    print(f"✅ Akkaunt ulandi: {me.first_name}")
    print("================================")
    print("24/7 online ishlayapti...")
    print("================================")
    
    # Bot ishga tushadi
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
