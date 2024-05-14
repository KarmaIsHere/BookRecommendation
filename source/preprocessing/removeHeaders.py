import os
import re


def remove_gutenberg_text(book_file):
    with open(book_file, 'r', encoding='utf-8') as f:
        text = f.read()

    # remove unconventional header
    uncon_header_keyword = "Project Gutenberg"
    uncon_header_end = text.find(uncon_header_keyword)
    if uncon_header_end > -1:
        text = text[uncon_header_end + len(uncon_header_keyword):]

    # remove the header
    header_keyword = "*END*THE SMALL PRINT"
    header_end = text.find(header_keyword)
    if header_end > -1:
        text = text[header_end + len(header_keyword):]

    # remove the footer
    footer_keyword = "Project Gutenberg"
    footer_start = text.find(footer_keyword)
    if footer_start > -1:
        text = text[:footer_start]

    # overwrite the book file with the modified text
    with open(book_file, 'w', encoding='utf-8') as f:
        f.write(text)


# indicates where your book .txt files are
# directory = './books'
#
# for filename in os.listdir(directory):
#     if filename.endswith('.txt'):
#         remove_gutenberg_text(os.path.join(directory, filename))
