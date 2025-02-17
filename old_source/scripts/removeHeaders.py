import os
import re


def remove_gutenberg_text(book_file):
    with open(book_file, 'r', encoding='utf-8') as f:
        text = f.read()

    clean_text = re.sub(r'\[\s*?Sidenote:*[\s\S]*?\]', '', text)
    clean_text = re.sub(r'\[\s*?Footnote:*[\s\S]*?\]', '', clean_text)
    clean_text = re.sub(r'\[\s*?Transcriber’s Note:*[\s\S]*?\]', '', clean_text)
    clean_text = re.sub(r'\[\s*?Illustration:*[\s\S]*?\]', '', clean_text)
    clean_text = re.sub(r'\[\s*?Note:*[\s\S]*?\]', '', clean_text)
    clean_text = re.sub(r'\[\[\s*?[\s\S]*?\]\]', '', clean_text)

    # overwrite the book file with the modified text
    with open(book_file, 'w', encoding='utf-8') as f:
        f.write(clean_text)


directory = '/mnt/d/Main/Uni/bakalauras/BookRecommendation/data/books'

for filename in os.listdir(directory):
    if filename.endswith('.txt'):
        remove_gutenberg_text(os.path.join(directory, filename))
