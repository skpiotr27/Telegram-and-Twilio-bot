from telethon.sync import TelegramClient

api_id =  "YOUR_API_ID"
api_hash = "YOUR_API_HASH"

with TelegramClient('anon', api_id, api_hash) as client:
        client.start()
