import os

import requests
from flask import Flask, render_template, redirect, url_for, request, flash, session
from routes.chatbot_routes import chatbot_bp
from utils.catalog import get_books_catalog


def create_app():
    app = Flask(__name__)
    app.register_blueprint(chatbot_bp)
    app.secret_key = os.getenv('FLASK_SECRET_KEY', 'fallback_key')

    SPRING_API_BASE_URL = 'http://localhost:8080'

    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/browse")
    def browse():
        limit = request.args.get("limit", default=12, type=int)
        books = get_books_catalog(limit=limit)
        return render_template("browse.html", books=books)

    @app.route('/book/<int:book_id>')
    def book_detail(book_id):
        return render_template('book_detail.html', book_id=book_id)

    @app.route("/recommendations")
    def recommendations():
        return render_template("recommendations.html")

    @app.route("/about")
    def about():
        return render_template("about.html")

    @app.route("/contact")
    def contact():
        return render_template("contact.html")

    @app.route("/my-books")
    def user_list():
        username = "Admin"
        try:
            response = requests.get(f"http://localhost:8080/api/user-book/get/{username}")
            response.raise_for_status()
            data = response.json()
            user_books = data.get("userBooks", [])
        except requests.RequestException as e:
            print(f"Error fetching user books: {e}")
            user_books = []

        return render_template("user_list.html", books=user_books, username=username)

    @app.route("/login", methods=['GET', 'POST'])
    def login():
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
                    session['username'] = username
                    flash('Login successful!')
                    return redirect(url_for('home'))
                else:
                    flash('Invalid credentials, please try again.')
                    return redirect(url_for('login'))
            except requests.exceptions.RequestException as e:
                flash(f"Failed to connect to authentication service: {str(e)}")
                return redirect(url_for('login'))

        return render_template('login.html')

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

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
