import json
import os

# Folder where .txt files are located
folder_path = '/mnt/d/Main/Uni/bakalauras/BookRecommendation/data/books'

# Open the JSON file
with open('/mnt/d/Main/Uni/bakalauras/BookRecommendation/data/filtered/books.json', 'r') as json_file:
    data = json.load(json_file)

    ids_checked = 0
    txt_files_count = len([f for f in os.listdir(folder_path) if f.endswith('.txt')])

    # Iterate over the JSON objects
    for item in data:
        # Construct the .txt file name
        file_name = str(item['id']) + '.txt'
        # Check for the file in the specified folder
        if not os.path.isfile(os.path.join(folder_path, file_name)):
            # Print out the id if the file does not exist
            print(item['id'])
        ids_checked += 1

    print(f"Checked {ids_checked} ids.")
    print(f"There are {txt_files_count} .txt files in the directory.")
