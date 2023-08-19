# Telegram-and-Twilio-bot

The bot I'm presenting was implemented in one of my projects. Its task was simple - if I have unread messages on Telegram (on a specific chat), then make a call using the Twilio API.

## Description of functions
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

