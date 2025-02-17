from flask import request

def process_and_print_response(payload):
    """Processes the Dialogflow response and prints user/bot messages."""
    user_message = payload['queryResult'].get('queryText', '')
    bot_message = payload['queryResult'].get('fulfillmentText', '')

    if user_message or bot_message:
        print(f"User: {user_message}")
        print(f"Bot: {bot_message}")
        return "Message received."
    else:
        print(request.data)
        return "200"
