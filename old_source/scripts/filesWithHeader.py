import os
import re
import subprocess

# Directory path
dir_path = '/data/books'


def search_files(directory, word):
    files_with_word = []

    # Loop over all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            # Open each .txt file
            try:
                with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                    content = file.read()
            except UnicodeDecodeError:
                print(f"Error decoding file: {filename}")

            # If word is found in file's content
            if re.search(word, content):
                files_with_word.append(filename)  # add file name to the list
                print(f"Found word in file: {filename}")  # print when word is found

    return files_with_word

target_string = 'Copyright'
files = search_files(dir_path, target_string)
print(files)
print(len(files))

for file in files:
    print(f"Opening {file}")
    subprocess.call(['notepad', os.path.join(dir_path, file)])  # This will wait until the notepad process is closed
