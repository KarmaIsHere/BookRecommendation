import pandas as pd


def preprocess_books(json_path):
    def cleanup_list(x):
        if isinstance(x, list):
            return " | ".join(map(str, x))
        else:
            return ""

    # Load data
    df = pd.read_json(json_path)

    # Convert the lists into strings
    df["authors_str"] = df["authors"].apply(cleanup_list)
    df["subjects_str"] = df["subjects"].apply(cleanup_list)
    df["bookshelves_str"] = df["bookshelves"].apply(cleanup_list)
    df["languages_str"] = df["languages"].apply(cleanup_list)

    # One-Hot Encoding
    df_one_hot_authors = df['authors_str'].str.get_dummies(sep=' | ')
    df_one_hot_subjects = df['subjects_str'].str.get_dummies(sep=' | ')
    df_one_hot_bookshelves = df['bookshelves_str'].str.get_dummies(sep=' | ')
    df_one_hot_languages = df['languages_str'].str.get_dummies(sep=' | ')

    # Combine the original data with the one-hot encoded data
    df_combined = pd.concat([
        df, df_one_hot_authors, df_one_hot_subjects,
        df_one_hot_bookshelves, df_one_hot_languages], axis=1)

    return df_combined


# Use like this
# df_combined = preprocess_books('/mnt/d/Main/Uni/bakalauras/BookRecommendation/data/filtered/books.json')
# print(df_combined.head())
# print(df_combined.info())
