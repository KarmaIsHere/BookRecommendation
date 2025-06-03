import os

import requests
from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from routes.chatbot_routes import chatbot_bp
from utils.catalog import get_books_catalog
from extensions import  login_manager
from flask_login import  login_user, logout_user, login_required

from utils.embeddings import generate_and_update_embeddings, fetch_all_book_ids


def create_app():
    app = Flask(__name__)
    app.register_blueprint(chatbot_bp)
    app.secret_key = os.getenv('FLASK_SECRET_KEY', 'fallback_key')

    login_manager.init_app(app)
    login_manager.login_view = 'login'

    from utils.models import User

    #SPRING_API_BASE_URL = 'https://bookrecommenddbserver.onrender.com'
    SPRING_API_BASE_URL = 'http://localhost:8080'
    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/browse")
    def browse():
        limit = request.args.get("limit", default=10, type=int)
        books = get_books_catalog(limit=limit, api_link=SPRING_API_BASE_URL)
        return render_template("browse.html", books=books, api=SPRING_API_BASE_URL)

    @app.route('/book/<int:book_id>')
    def book_detail(book_id):
        return render_template('book_detail.html', book_id=book_id, username=getattr(current_user, 'id', None),
                               api=SPRING_API_BASE_URL)

    @app.route("/recommendations")
    @login_required
    def recommendations():
        return render_template("recommendations.html")

    # @app.route("/recommendations")
    # @login_required
    # def recommendations():
    #     username = current_user.id
    #     try:
    #         response = requests.get(f"{SPRING_API_BASE_URL}/api/user-book/get/{username}")
    #         response.raise_for_status()
    #         data = response.json()
    #         recommendations = data.get("recommendations", [])
    #     except requests.RequestException as e:
    #         print(f"Error fetching user books: {e}")
    #         recommendations = []
    #
    #     return render_template("recommendations.html", recommendations=recommendations, username=username)

    @app.route("/about")
    def about():
        return render_template("about.html")

    @app.route("/contact")
    def contact():
        return render_template("contact.html")

    @app.route("/my-books")
    @login_required
    def user_list():
        username = current_user.id
        try:
            response = requests.get(f"{SPRING_API_BASE_URL}/api/user-book/get/{username}")
            response.raise_for_status()
            data = response.json()
            user_books = data.get("userBooks", [])
        except requests.RequestException as e:
            print(f"Error fetching user books: {e}")
            user_books = []

        return render_template("user_list.html", books=user_books, username=username)

    from flask_login import current_user

    @app.route("/login", methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('home'))

        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            user_data = {
                "username": username,
                "password": password
            }

            try:
                response = requests.post(f"{SPRING_API_BASE_URL}/api/login", json=user_data)
                if response.status_code == 200:
                    user = User(username)
                    login_user(user)
                    return redirect(url_for('home'))
                else:
                    flash('Invalid credentials, please try again.')
                    return redirect(url_for('login'))
            except requests.exceptions.RequestException as e:
                flash(f"Failed to connect to authentication service: {str(e)}")
                return redirect(url_for('login'))

        return render_template('login.html')

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash("Logged out.")
        return redirect(url_for("login", _scheme='http', _external=True))

    @app.route("/register", methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')

            user_data = {
                "username": username,
                "email": email,
                "password": password
            }

            try:
                response = requests.post(f"{SPRING_API_BASE_URL}/api/user/create", json=user_data)

                if response.status_code in [200, 201]:
                    flash('Registration successful!')
                    return redirect(url_for('login'))
                else:

                    try:
                        error_data = response.json()
                        for field, message in error_data.items():
                            flash(f"{message}", "error")
                    except ValueError:
                        flash("An error occurred during registration.", "error")
                    return redirect(url_for('register'))
            except requests.exceptions.RequestException as e:
                flash(f"Failed to connect to registration service: {str(e)}", "error")
                return redirect(url_for('register'))

        return render_template('register.html')

    @app.route('/update-embeddings', methods=['POST'])
    def update_embeddings():
        book_ids = fetch_all_book_ids(SPRING_API_BASE_URL)
        result = generate_and_update_embeddings(book_ids, SPRING_API_BASE_URL)
        return jsonify(result)

    @app.route('/fetch-books', methods=['GET'])
    def fetch_books_from_spring():
        try:
            response = requests.get(f"{SPRING_API_BASE_URL}/api/fetch-books")
            response.raise_for_status()
            return response.text, response.status_code
        except requests.exceptions.RequestException as e:
            return f"Failed to connect to book fetching service: {str(e)}", 500

    @app.route("/admin-tools")
    @login_required
    def admin_tools():
        return render_template("admin_tools.html")

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
