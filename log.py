from telethon.sync import TelegramClient

# Set your API data
api_id =  "YOUR_API_ID"
api_hash = "YOUR_API_HASH"

# Generate anon.session and save it
with TelegramClient('anon', api_id, api_hash) as client:
        client.start()
