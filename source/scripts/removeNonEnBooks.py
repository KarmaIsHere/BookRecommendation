import json
import os

# Load the book data
with open("/mnt/d/Main/Uni/bakalauras/BookRecommendation/data/filtered/books.json", "r") as read_file:
    data = json.load(read_file)

# Directory containing .txt files
dir_path = "/mnt/d/Main/Uni/bakalauras/BookRecommendation/data/books"

# New list to hold books that include 'en' in their 'languages' list
filtered_data = []

# Check each book in the data
for book in data:
    # If the book's 'languages' list includes 'en'
    if 'languages' in book and 'en' in book['languages']:
        # Add the book to the filtered_data list
        filtered_data.append(book)
    else:
        # Format book id into .txt file name
        book_filename = "{}.txt".format(book['id'])
        # Combine directory path with file name to get full file path
        file_path = os.path.join(dir_path, book_filename)

        # Check if file exists before attempting to remove it
        if os.path.isfile(file_path):
            # Remove the .txt file
            os.remove(file_path)
            print(f'Removed: {file_path}')

# Write the modified book data back to the .json file
with open("/mnt/d/Main/Uni/bakalauras/BookRecommendation/data/filtered/books_filtered.json", "w") as write_file:
    json.dump(filtered_data, write_file)

print("Completed filtering of book files and JSON data.")
