import json
from twilio.rest import Client
from telethon.sync import TelegramClient
import os
import shutil
import time

# Download data from environ from AWS Lambda
api_id = os.environ.get('API_ID') 
api_hash = os.environ.get('API_HASH') 
twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
twilio_auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
twilio_phone_number = os.environ.get('TWILIO_PHONE_NUMBER')
destination_phone_number = os.environ.get('DESTINATION_PHONE_NUMBER')
name_of_chat = os.environ.get('NAME_OF_TELEGRAM_CHAT')


 
def lambda_handler(event,context):
    """ Handler function for AWS Lambda that checks for unread messages in a Telegram chat
    and makes a call via Twilio to notify the user if there are any unread messages.
    
    The function calls the `produce_result` function three times with a 20-second interval
    between each call. This is to ensure multiple checks and notifications within a single 
    Lambda execution.

    Parameters:
    - event (dict): Event data passed to the handler (not used in the function).
    - context (LambdaContext): Runtime information provided by AWS Lambda.

    Returns:
    - dict: Result from the last call to the `produce_result` function, typically containing
            the HTTP status code and a response message.
            
    Note:
    Ensure that all the required parameters for `produce_result` (like `api_id`, `api_hash`, etc.)
    are defined and accessible within the scope of this function. """
    
    produce_result(api_id,api_hash,twilio_account_sid,twilio_auth_token,twilio_phone_number,destination_phone_number,name_of_chat)
    time.sleep(20)
    produce_result(api_id,api_hash,twilio_account_sid,twilio_auth_token,twilio_phone_number,destination_phone_number,name_of_chat)
    time.sleep(20)
    return produce_result(api_id,api_hash,twilio_account_sid,twilio_auth_token,twilio_phone_number,destination_phone_number,name_of_chat)


def produce_result(api_id, api_hash, account_sid, auth_token, twilio_phone_number, to_phone_number, name_of_chat):
    """ Check for unread messages in a specific Telegram chat. If there are unread messages,
    place a call via Twilio to notify the user.

    Parameters:
    - api_id (str): The API ID for Telegram.
    - api_hash (str): The API hash for Telegram.
    - account_sid (str): The account SID for Twilio.
    - auth_token (str): The authentication token for Twilio.
    - twilio_phone_number (str): The phone number from which the call will be placed using Twilio.
    - to_phone_number (str): The destination phone number to which the call will be placed.
    - name_of_chat (str): The name of the Telegram chat to check for unread messages.

    Returns:
    - dict: An HTTP response dictionary, typically used in AWS Lambda functions."""
    
    # Initialize unread status as False
    is_unread = False

    # Copy the 'anon.session' file to the '/tmp' directory, which is writable in AWS Lambda environment
    shutil.copy2('anon.session', '/tmp/anon.session')

    # Path for the session file
    session_file_path = '/tmp/anon.session'
    
    # Create a Telegram client using the provided session file, api_id, and api_hash
    with TelegramClient(session_file_path, api_id, api_hash) as client:
        # Iterate over all dialogs (chats) in the Telegram client
        for dialog in client.iter_dialogs():
            # Check if there are unread messages in the chat
            if dialog.unread_count > 0:
                # Check if the name of the chat matches the specified chat name
                if dialog.name == name_of_chat:
                    is_unread = True
                
    # If there are unread messages in the specified chat
    if is_unread:
        # Create a Twilio client using the provided account_sid and auth_token
        client = Client(account_sid, auth_token)

        # Place a call using the Twilio client
        call = client.calls.create(
            twiml='<Response><Say>Hello, you have unread messages on Telegram.</Say></Response>',
            to=to_phone_number,
            from_=twilio_phone_number
        )
        
        # Print the result of the call
        print(f"I've called the number {to_phone_number} with a message about unread messages on Telegram. Call ID: {call.sid}")
    else:
        # If all messages are read, print a message indicating that
        print("All messages read")

    # Return an HTTP response, typically for AWS Lambda
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

