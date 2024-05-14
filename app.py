from flask import Flask
from routes import set_dialog_flow_route


def create_app():
    app = Flask(__name__)
    set_dialog_flow_route(app)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
