import requests

def get_books_catalog(limit, api_link):
    page = 0
    collected_books = []

    while len(collected_books) < limit:
        try:
            response = requests.get(
                f"{api_link}/api/book/books",
                params={"page": page, "size": limit}
            )
            response.raise_for_status()
            data = response.json()

            for item in data["books"]:
                title = item.get("title", "Untitled")
                authors = ", ".join(item.get("authors", ["Unknown Author"]))
                collected_books.append({"Title": title, "Authors": authors})
                if len(collected_books) >= limit:
                    break

            if data["currentPage"] + 1 >= data["totalPages"]:
                break

            page += 1

        except requests.RequestException as e:
            print(f"Error fetching books: {e}")
            break

    return collected_books[:limit]
