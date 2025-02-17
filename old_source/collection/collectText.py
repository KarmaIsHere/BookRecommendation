import json
import os
import zlib
from tqdm import tqdm

import gutenbergpy.textget


# download_and_store_books_from_json('data/filtered/books.json', 'data/books')

def download_and_store_books_from_json(json_file, directory):
    # Load book ids from json
    with open(json_file, 'r') as f:
        books_metadata = json.load(f)

    successful_downloads = 0

    # Download each book by id and store them in a separate text file
    for book_metadata in tqdm(books_metadata, desc='Downloading books', unit='book'):
        book_id = book_metadata['id']
        try:
            raw_book = gutenbergpy.textget.get_text_by_id(book_id)
            clean_book_bytes = gutenbergpy.textget.strip_headers(raw_book)
            clean_book = clean_book_bytes.decode('utf-8')

            # Create the directory if it doesn’t exist
            if not os.path.exists(directory):
                os.makedirs(directory)

            # Save the book to a file
            with open(os.path.join(directory, f'{book_id}.txt'), 'w', encoding='utf-8') as file:
                file.write(clean_book)

            successful_downloads += 1

        except Exception as e:
            print(f"Failed to download and save book id {book_id}. Reason: {e}")
        except zlib.error as zerr:
            print(f"Failed to download and save book id {book_id} due to zlib error: {zerr}")

    print(f"\nTotal number of books successfully downloaded: {successful_downloads}")
