![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Twilio)
![Framework Name](https://img.shields.io/badge/frameworkName-aws--cdk-green)



# Telegram-and-Twilio-bot

The bot I'm presenting was implemented in one of my projects. Its task was simple - if I have unread messages on Telegram (on a specific chat), then make a call using the Twilio API.

## Description of functions

## `log.py` Function

This script provides a basic demonstration of connecting to the Telegram API using the Telethon Python library. It initiates a connection to Telegram and starts a client session.

### Prerequisites

- Telethon library: Install it using pip:
  ```
  pip install telethon
  ```

### Configuration

- **api_id**: Your unique API ID provided by Telegram. You can obtain it by registering your app at [Telegram's developer portal](https://my.telegram.org/auth).
- **api_hash**: Your unique API hash provided alongside the `api_id`.

Replace `"YOUR_API_ID"` and `"YOUR_API_HASH"` in the code with your actual credentials.

### Execution

1. Ensure the Telethon library is installed and the above configurations are set.
2. Run the script. On the first run, you'll be prompted to enter your phone number and a verification code sent to your Telegram account. This establishes the 'anon' session.
3. Subsequent runs will use the 'anon' session and won't prompt for the phone number or verification code.

### Notes:

- The script uses an 'anon' session, which means session data will be stored locally in a file named 'anon.session'. Handle this file with care as it contains session data.
- Make sure not to share your `api_id` and `api_hash` as they are sensitive credentials.

---


## `produce_result` Function

This function is designed to monitor unread messages in a specific chat on Telegram. If there are any unread messages, the function initiates a phone call through Twilio, notifying the user about the unread messages.

### Parameters:

- **api_id**: Your `api_id` from Telegram.
- **api_hash**: Your `api_hash` from Telegram.
- **account_sid**: Your `account_sid` from Twilio.
- **auth_token**: Your `auth_token` from Twilio.
- **twilio_phone_number**: The Twilio phone number from which the call will be made.
- **to_phone_number**: The destination phone number to which the call will be placed.
- **name_of_chat**: The name of the Telegram chat you wish to monitor.

### Return Value:

Returns a dictionary with the following structure:
```python
{
    'statusCode': 200,
    'body': json.dumps('Hello from Lambda!')
}
```

### Notes:

1. The function uses the `TelegramClient` library to connect to Telegram and check for unread messages.
2. If there are unread messages, it utilizes the Twilio API to make a phone call.
3. The function assumes the presence of an 'anon.session' session file, which gets copied to `/tmp/anon.session` prior to its use.
4. Ensure you have all necessary dependencies installed before using this function.


---

## `lambda_handler` Function

The `lambda_handler` function is designed to be triggered by AWS Lambda events. It calls the `produce_result` function three times with a 20-second delay between each invocation. The requirement was that the script should check for unread messages every 20 seconds or so. Unfortunately, AWS does not anticipate launching the feature in such a short period of time. The lowest period is 1 minute, so the function runs the function that checks the telegram three times every 20 seconds

### Parameters:

- **event**: The triggering event data for the AWS Lambda function.
- **context**: The runtime information for the AWS Lambda function.

### Behavior:

1. Calls the `produce_result` function with predefined parameters.
2. Waits for 20 seconds using `time.sleep(20)`.
3. Calls the `produce_result` function again with the same parameters.
4. Waits for another 20 seconds.
5. Calls the `produce_result` function a final time with the same parameters and returns its result.

### Dependencies:

- Ensure that the `produce_result` function is available and properly set up.
- Ensure that all global parameters (like `api_id`, `api_hash`, etc.) are correctly defined in the environment or as global variables in your code.

### Notes:

- This function is intended to be used as an AWS Lambda handler. Ensure you have configured your Lambda environment correctly to use it.
- The function assumes that all parameters needed for `produce_result` are available as global or environmental variables.
- Make sure the total execution time (including sleep intervals) does not exceed the timeout configured for your AWS Lambda function.

---

# Implementation on Amazon Web Services (AWS).

To deploy the script on AWS, you need to upload a ZIP file containing all the utilized libraries as well as the `lambda_function` script and `anon.session` generated using `log.py`. The `AWS files.zip` contains all the necessary files except for `anon.session`. If you want to use this script, just generate `anon.session` and add it to the zip file, then upload the file to AWS.

Of course, if you prefer, you can install all the required libraries and bundle them along with `lambda_function.py` into a ZIP file. In that case, I recommend using environments, like Anaconda, to create a new environment and then install only the required libraries and bundle them.

Remember that on AWS, you need to add the following environment variables: 
```python
api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')
twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
twilio_auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
twilio_phone_number = os.environ.get('TWILIO_PHONE_NUMBER')
destination_phone_number = os.environ.get('DESTINATION_PHONE_NUMBER')
name_of_chat = os.environ.get('NAME_OF_TELEGRAM_CHAT')
```

And you need to set a trigger. I set mine to 1M because I want the function to run 3 times a minute, every 20 seconds.
