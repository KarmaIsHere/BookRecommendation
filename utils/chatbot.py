from flask import request, jsonify


def process_and_print_response(payload):
    user_message = payload['queryResult'].get('queryText', '')
    bot_message = payload['queryResult'].get('fulfillmentText', '')

    parameters = payload['queryResult'].get('parameters', {})
    person = parameters.get('person', [])
    author = person[0].get('name') if person else None

    print(f"User: {user_message}")
    print(f"Bot: {bot_message}")
    print (parameters)


    if author:
        recommended_book = recommend_book("Fantasy", author)
        return jsonify({
            "followupEventInput": {
                "name": "recommendation_ready",
                "languageCode": "en",
                "parameters": {
                    "book": recommended_book
                }
            }
        })

    return jsonify({
        "fulfillmentText": bot_message
    })

def recommend_book(genre, author):
    return "Crime and Punishment"
