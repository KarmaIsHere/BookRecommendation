import time
import requests
import json
from flask import request, jsonify

COUNT = 500
API_URL = 'https://gutendex.com/books'
DATA_PATH = '../../data/raw/books_data.json'
FILTER_PATH = '../../data/filtered/books.json'


# run_book_data_collection(app)

def run_book_data_collection(app): # runs book collection
    register_book_routes(app)
    save_books_to_file()


def fetch_books_from_api():
    params = {}
    books_data = {
        'count': 0,
        'next': API_URL,
        'previous': None,
        'results': []
    }
    try:
        while books_data['next'] and len(books_data['results']) < COUNT:
            response = requests.get(books_data['next'], params=params)
            response.raise_for_status()
            page_data = response.json()
            books_data['count'] = page_data['count']
            books_data['next'] = page_data['next']
            books_data['previous'] = page_data['previous']
            books_data['results'].extend(page_data['results'])
            time.sleep(1)  # To avoid potential rate limiting
        if len(books_data['results']) > COUNT:
            books_data['results'] = books_data['results'][:COUNT]
        return books_data, 200
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}, 500


def register_book_routes(app):
    @app.route('/get_books', methods=['GET'])
    def get_books():
        books_data, status_code = fetch_books_from_api()
        return jsonify(books_data), status_code


def save_books_to_file():
    books_data, status_code = fetch_books_from_api()
    if status_code == 200:
        with open(DATA_PATH, 'w') as f:
            json.dump(books_data, f)
        filter_and_save_book_data(books_data)
    else:
        print(f"An error occurred: {books_data.get('error')}")


def filter_and_save_book_data(books_data):
    results = books_data.get('results', [])
    output = []
    for book in results:
        authors = [author['name'] for author in book.get('authors', [])]
        book_info = {
            'id': book.get('id'),
            'title': book.get('title'),
            'authors': authors,
            'subjects': book.get('subjects', []),
            'bookshelves': book.get('bookshelves', []),
            'languages': book.get('languages', [])
        }
        output.append(book_info)
    with open(FILTER_PATH, 'w') as f:
        json.dump(output, f)
