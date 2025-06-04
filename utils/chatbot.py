from flask import request, jsonify

from utils.recommendation import recommend_book


def process_and_print_response(payload):
    user_message = payload['queryResult'].get('queryText', '')
    bot_message = payload['queryResult'].get('fulfillmentText', '')

    parameters = payload['queryResult'].get('parameters', {})
    output_contexts = payload['queryResult'].get('outputContexts', [])

    genre = parameters.get('genre')
    if isinstance(genre, list) and genre:
        genre = genre[0]

    person = parameters.get('person', [])
    author = person[0].get('name') if person and isinstance(person, list) else None

    for ctx in output_contexts:
        ctx_params = ctx.get('parameters', {})

        if not genre:
            g = ctx_params.get('genre')
            if isinstance(g, list) and g:
                genre = g[0]
            elif isinstance(g, str):
                genre = g

        if not author:
            p = ctx_params.get('person')
            if isinstance(p, list) and p:
                author = p[0].get('name')
            elif isinstance(p, dict):
                author = p.get('name')

    # print(f"User: {user_message}")
    # print(f"Bot: {bot_message}")
    # print(f"Extracted genre: {genre}")
    # print(f"Extracted author: {author}")

    if genre and author:
        recommended_book = recommend_book(genre, author)
        return jsonify({
            "followupEventInput": {
                "name": "recommendation_ready",
                "languageCode": "en",
                "parameters": {
                    "book": recommended_book
                }
            },
            "outputContexts": [
                {
                    "name": f"{payload['session']}/contexts/awaiting_author",
                    "lifespanCount": 0
                }
            ]
        })

    return jsonify({
        "fulfillmentText": bot_message
    })

