import numpy as np
from numpy.linalg import norm

from utils.embeddings import create_embedding
from utils.embeddings import fetch_all_book_embeddings

SPRING_API_BASE_URL = 'https://bookrecommenddbserver.onrender.com'
#SPRING_API_BASE_URL = 'http://localhost:8080'

def cosine_similarity(vec1, vec2):
    if vec1 is None or vec2 is None:
        return -1
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    if norm(vec1) == 0 or norm(vec2) == 0:
        return -1
    return np.dot(vec1, vec2) / (norm(vec1) * norm(vec2))

def recommend_book(genre, author):
    query_text = f"I'm looking for a {genre} book written by {author}."
    query_embedding = create_embedding(query_text)
    if not query_embedding:
        return "Sorry, could not process your input for recommendations."

    book_embeddings_list = fetch_all_book_embeddings(genre, author, SPRING_API_BASE_URL)
    if not book_embeddings_list:
        return "No book data available for recommendations based on your criteria."

    best_book_id = None
    best_score = -1
    best_book_title = "A recommended book"

    for book_data in book_embeddings_list:
        book_id = book_data.get("book_id")
        embedding = book_data.get("embedding")
        title = book_data.get("title")

        if book_id is None or embedding is None:
            print(f"Warning: Missing book_id or embedding in book_data: {book_data}")
            continue

        score = cosine_similarity(query_embedding, embedding)
        if score > best_score:
            best_score = score
            best_book_id = book_id
            best_book_title = title if title is not None else "A recommended book"

    if best_book_id:
        return best_book_title
    else:
        return "No suitable recommendation found."