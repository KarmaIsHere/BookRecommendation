from flask import Blueprint, request
from utils.chatbot import process_and_print_response

# Define the chatbot blueprint
chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/webhook', methods=["POST", "GET"])
def webhook(): # Handles GET requests for testing and POST requests for Dialogflow fulfillment.
    if request.method == "GET":
        return "Hello, World!"  # Test GET request
    elif request.method == "POST":
        payload = request.json  # Get the JSON payload from Dialogflow
        return process_and_print_response(payload)
