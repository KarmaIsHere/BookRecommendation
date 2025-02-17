import pandas as pd

def get_books_catalog(limit):
    get_catalog = True

    if get_catalog:
        df_books_catalog = pd.read_csv('https://www.gutenberg.org/cache/epub/feeds/pg_catalog.csv', keep_default_na=False)
        df_books_catalog = df_books_catalog[df_books_catalog['Language'] == 'en']
        df_books_catalog.reset_index(drop=True, inplace=True)

    df_books_catalog['Authors'] = df_books_catalog['Authors'].fillna('Unknown Author')

    books = df_books_catalog[['Title', 'Authors']].head(limit).to_dict(orient='records')

    return books