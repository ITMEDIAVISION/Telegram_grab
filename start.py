pip install --upgrade pip
import os
import asyncio
from telethon import TelegramClient, events
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.errors import FloodWaitError

api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
bot_token = 'YOUR_BOT_TOKEN'

client = TelegramClient('telegram_export_bot', api_id, api_hash).start(bot_token=bot_token)

async def download_media(message):
    media = message.media
    if media is not None:
        try:
            await client.download_media(media, 'exported_files')
        except Exception as e:
            print(f"Error downloading media: {e}")

async def export_chat(event):
    chat = await event.get_chat()
    limit = 100  # Number of messages to fetch at once
    offset_id = 0
    all_messages = []
    
    while True:
        try:
            history = await client(GetHistoryRequest(
                peer=chat,
                offset_id=offset_id,
                offset_date=None,
                add_offset=0,
                limit=limit,
                max_id=0,
                min_id=0,
                hash=0
            ))
            if not history.messages:
                break
            all_messages.extend(history.messages)
            offset_id = all_messages[-1].id
            print(f"Retrieved {len(all_messages)} messages")
            for message in history.messages:
                await download_media(message)
                
        except FloodWaitError as e:
            print(f"Sleeping for {e.seconds} seconds")
            await asyncio.sleep(e.seconds)

@client.on(events.NewMessage(pattern='/export'))
async def handle_export_command(event):
