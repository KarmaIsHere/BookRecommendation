import requests
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

def create_embedding(text):
    if not text:
        return None
    return embedding_model.encode(text).tolist()

def fetch_all_book_ids(SPRING_API_BASE_URL):
    try:
        response = requests.get(f"{SPRING_API_BASE_URL}/api/book/all-ids")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching book IDs: {e}")
        return []

def fetch_all_book_embeddings(genre, author, SPRING_API_BASE_URL):
    try:
        response = requests.get(f"{SPRING_API_BASE_URL}/api/book/all-embeddings/{genre}/{author}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching book embeddings: {e}")
        return {}

def generate_and_update_embeddings(book_ids, SPRING_API_BASE_URL):
    results = []
    for book_id in book_ids:
        try:
            response = requests.get(f"{SPRING_API_BASE_URL}/api/book/details/{book_id}")
            response.raise_for_status()
            book = response.json()
            summary = book.get("summary", "")

            embedding = create_embedding(summary)

            if embedding:
                update_response = requests.put(
                    f"{SPRING_API_BASE_URL}/api/book/up/embedding/{book_id}",
                    json=embedding,
                    headers={'Content-Type': 'application/json'}
                )

                if update_response.status_code == 200:
                    results.append({"book_id": book_id, "status": "updated"})
                else:
                    results.append({"book_id": book_id, "status": "failed to update"})
            else:
                results.append({"book_id": book_id, "status": "no summary or failed embedding"})
        except requests.RequestException as e:
            results.append({"book_id": book_id, "status": f"error: {e}"})
    return results
