import os
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

os.environ["TFHUB_CACHE_DIR"] = '/tfhub'

nltk.download('wordnet')
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()


def get_book_content(book_id):
    with open(f"/mnt/d/Main/Uni/bakalauras/BookRecommendation/data/books/{book_id}.txt", 'r') as f:
        for line in f:
            yield line.strip()


def preprocess_text(line):
    line = line.lower()
    tokens = word_tokenize(line)
    tokens = [word for word in tokens if word.isalpha() and not word in stop_words]
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return tokens  # return a list of tokens


def process_book(book):
    for line in get_book_content(book['id']):
        yield preprocess_text(line)
