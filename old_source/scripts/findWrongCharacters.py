import string
import os

# Define acceptable characters
acceptable_chars = set(
    string.ascii_lowercase + string.ascii_uppercase + string.digits + ' ' + '\n' + string.punctuation)

# Define data path
data_path = "/mnt/d/Main/Uni/bakalauras/BookRecommendation/data/books/"

# Check each file for unacceptable characters
for book_filename in os.listdir(data_path):
    with open(data_path + book_filename, 'r', encoding='utf-8') as book_file:
        content = book_file.read()
        for character in content:
            if character not in acceptable_chars:
                print(f"Found unacceptable character '{character}' in {book_filename}")