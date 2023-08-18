import json
from twilio.rest import Client
from telethon.sync import TelegramClient
import os
import shutil
import time


api_id = os.environ.get('API_ID') 
api_hash = os.environ.get('API_HASH') 
twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
twilio_auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
twilio_phone_number = os.environ.get('TWILIO_PHONE_NUMBER')
destination_phone_number = os.environ.get('DESTINATION_PHONE_NUMBER')
name_of_chat = os.environ.get('NAME_OF_TELEGRAM_CHAT')



def lambda_handler(event,context):
    produce_result(api_id,api_hash,twilio_account_sid,twilio_auth_token,twilio_phone_number,destination_phone_number,name_of_chat)
    time.sleep(20)
    produce_result(api_id,api_hash,twilio_account_sid,twilio_auth_token,twilio_phone_number,destination_phone_number,name_of_chat)
    time.sleep(20)
    return produce_result(api_id,api_hash,twilio_account_sid,twilio_auth_token,twilio_phone_number,destination_phone_number,name_of_chat)


def produce_result(api_id, api_hash, account_sid, auth_token, twilio_phone_number, to_phone_number,name_of_chat):
    is_unread = False

    shutil.copy2('anon.session', '/tmp/anon.session')

    session_file_path = '/tmp/anon.session'
    with TelegramClient(session_file_path, api_id, api_hash) as client:
        for dialog in client.iter_dialogs():
            if dialog.unread_count > 0:
                if dialog.name == name_of_chat:
                    is_unread = True
                
    if is_unread:
        client = Client(account_sid, auth_token)

        call = client.calls.create(
            twiml='<Response><Say>Hello, you have unread messages on Telegram.</Say></Response>',
            to= to_phone_number,
            from_=twilio_phone_number
        )
        print(f"I've called the number {to_phone_number} with a message about unread messages on Telegram. Call ID: {call.sid}")
    else:
        print("All messages read")
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
