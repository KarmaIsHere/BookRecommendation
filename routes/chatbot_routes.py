from flask import Blueprint, request
from utils.chatbot import process_and_print_response
chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/webhook', methods=["POST", "GET"])
def webhook():
    if request.method == "GET":
        return "Hello, World!"
    elif request.method == "POST":
        payload = request.json
        return process_and_print_response(payload)
