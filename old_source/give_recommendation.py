import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


from old_source.train_book_recommendation import vectorizer, shared_lstm, shared_embedding


def recommend_books(genre, author, n_recommendations=10):
    # Filter the relevant books based on the given genre and author.
    relevant_books = [book for book in data
                      if genre in book['bookshelves'] and author in book['authors']]

    if not relevant_books:
        print('No matches found')
        return

    # Embed the relevant books using your model
    relevant_books_contents = [book['text'] for book in relevant_books]
    relevant_books_encoded = vectorizer(relevant_books_contents)
    relevant_books_embeddings = shared_lstm(shared_embedding(relevant_books_encoded))


    # Calculate similarity scores with all other books
    similarity_scores = cosine_similarity(relevant_books_embeddings, book_embeddings)

    # Get the indices of the books with the highest similarity scores
    recommended_books_indices = np.argpartition(similarity_scores, -n_recommendations)[-n_recommendations:]

    # Fetch the recommended books from your metadata
    recommended_books = [data[i] for i in recommended_books_indices]

    return recommended_books
