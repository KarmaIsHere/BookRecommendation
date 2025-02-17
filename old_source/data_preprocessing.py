import os
import json
import gc
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.preprocessing import MultiLabelBinarizer
from tensorflow.keras.layers import TextVectorization
import pickle

# Specify matplotlib backend
os.environ["TFHUB_CACHE_DIR"] = '/tfhub'

nltk.download('wordnet')
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()
mlb_authors = MultiLabelBinarizer()
mlb_genres = MultiLabelBinarizer()
vectorizer = TextVectorization(max_tokens=20000, output_sequence_length=100)
num_books = 300


def safe_decode(text, encoding='utf-8'):
    return text.decode(encoding, errors='ignore')


def preprocess_text(line):
    line = line.lower()
    tokens = word_tokenize(line)
    tokens = [word for word in tokens if word.isalpha() and not word in stop_words]
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return ' '.join(tokens)  # Return a single string


def process_books_chunk(books_data, start, end):
    books = []
    authors = []
    genres = []
    # Extract the authors, genres, and book contents
    for book in books_data[start:end]:
        genres.append(book['bookshelves'])  # Keep it as a list
        authors.append(book['authors'])  # Keep it as a list
        with open(f"/mnt/d/Main/Uni/bakalauras/BookRecommendation/data/books/{book['id']}.txt", 'rb') as f:
            text_content = f.read()
            text_content_decoded = safe_decode(text_content)
            if text_content_decoded.strip():  # This will be False for empty or whitespace strings
                books.append(preprocess_text(text_content_decoded))
    return books, authors, genres


books_data = "/mnt/d/Main/Uni/bakalauras/BookRecommendation/data/filtered/books.json"
with open(books_data, "r") as f:
    data = json.load(f)

# Select only 300 books
data = data[:num_books]

chunk_size = 50  # Adjust this value based on your available memory

num_chunks = (len(data) + chunk_size - 1) // chunk_size  # ceil division

for i in range(num_chunks):
    start = i * chunk_size
    end = min(start + chunk_size, len(data))
    print(f"Processing books {start} to {end}")

    books_chunk, authors_chunk, genres_chunk = process_books_chunk(data, start, end)

    # Fit MultiLabelBinarizer before the transformation
    mlb_authors.fit(authors_chunk)
    mlb_genres.fit(genres_chunk)

    vectorizer.adapt(books_chunk)

    books_encoded = vectorizer(books_chunk)

    # Now you can transform your data
    authors_encoded = mlb_authors.transform(authors_chunk)
    genres_encoded = mlb_genres.transform(genres_chunk)

    with open(f'/mnt/d/Main/Uni/bakalauras/BookRecommendation/source/preprocessing/preprocessed_data_chunk_{num_books}.pkl',
              'wb') as f:
        pickle.dump([books_encoded, genres_encoded, authors_encoded, vectorizer.get_vocabulary()], f)

    del books_chunk, authors_chunk, genres_chunk, books_encoded, authors_encoded, genres_encoded
    gc.collect()
