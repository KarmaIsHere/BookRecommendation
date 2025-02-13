from flask import request


def process_and_print_response(payload):
    user_message = payload['queryResult']['queryText']
    bot_message = payload['queryResult']['fulfillmentText']
    if user_message or bot_message != "":
        print(f"User: {user_message}")
        print(f"Bot: {bot_message}")
        return "Message received."
    else:
        print(request.data)
        return "200"


def set_dialog_flow_route(app):
    @app.route('/', methods=["POST", "GET"])
    def webhook():
        if request.method == "GET":
            return "Hello, World!"
        elif request.method == "POST":
            payload = request.json
            return process_and_print_response(payload)
