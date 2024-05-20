import json


def remove_books(json_file, remove_ids):
    # Load book ids from json
    with open(json_file, 'r') as f:
        books_metadata = json.load(f)

    # Filter books_metadata to remove unwanted books
    books_metadata = [book for book in books_metadata if book['id'] not in remove_ids]

    # Save the modified books_metadata back to json
    with open(json_file, 'w') as f:
        json.dump(books_metadata, f)
