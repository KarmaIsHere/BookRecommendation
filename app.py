from flask import Flask, request, jsonify
from source.fulfillment.routes import set_dialog_flow_route
from source.give_recommendation import recommend_books


def create_app():
    app = Flask(__name__)
    set_dialog_flow_route(app)
    @app.route('/recommendation', methods=['POST'])
    def recommendation():
        # Extract genre and author from request
        data = request.get_json()
        genre = data['genre']
        author = data['author']

        # Get recommendation
        recommendation = recommend_books(genre, author)

        # Prepare response
        response = {
            'fulfillmentText': recommendation
        }

        return jsonify(response)
    return app




if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
