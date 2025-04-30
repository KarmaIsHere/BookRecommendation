from flask import Flask, render_template, redirect, url_for, request
from routes.chatbot_routes import chatbot_bp
from utils.catalog import get_books_catalog


def create_app():
    app = Flask(__name__)
    app.register_blueprint(chatbot_bp)  # Register chatbot blueprint

    @app.route("/home")
    def home():
        return render_template("index.html")

    @app.route("/browse")
    def browse():
        limit = request.args.get("limit", default=12, type=int)  # Get limit from query string
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

    @app.route("/login", methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            print(f"Username: {username}, Password: {password}")
            return redirect(url_for('home'))
        return render_template('login.html')

    @app.route("/register", methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            print(f"Username: {username}, Email: {email}, Password: {password}")
            return redirect(url_for('login'))
        return render_template('register.html')

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
