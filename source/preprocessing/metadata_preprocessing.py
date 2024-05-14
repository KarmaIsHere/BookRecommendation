import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
# Load data
df = pd.read_json('../../data/filtered/books.json')

# Data Cleaning
# convert any non-list values to an empty list
df[['authors', 'subjects', 'bookshelves', 'languages']] = df[
    ['authors', 'subjects', 'bookshelves', 'languages']].applymap(lambda x: x if type(x) == list else [])

# Splitting the title into 'title' and 'subtitle'
df[['title', 'subtitle']] = df['title'].str.split('; Or,', n=1, expand=True)

# Stripping leading/trailing white spaces that might be introduced during splitting
df['title'] = df['title'].str.strip()
df['subtitle'] = df['subtitle'].str.strip()

# Replace NaN with empty strings if no subtitle exists
df['subtitle'].fillna('', inplace=True)

# Feature Engineering
# create count features
df['num_authors'] = df['authors'].apply(len)
df['num_subjects'] = df['subjects'].apply(len)
df['num_bookshelves'] = df['bookshelves'].apply(len)
df['num_languages'] = df['languages'].apply(len)
df['title_length'] = df['title'].apply(len)

# Convert list of languages to string type, as get_dummies() does not work with list type
df['languages'] = df['languages'].apply(lambda x: ', '.join(x))

# Apply One-Hot Encoding
df_languages = pd.get_dummies(df['languages'].str.get_dummies(sep=', '))

# Convert the lists into strings
df["authors"] = df["authors"].apply(lambda x: " ".join(x))
df["subjects"] = df["subjects"].apply(lambda x: " ".join(x))
df["bookshelves"] = df["bookshelves"].apply(lambda x: " ".join(x))

# Combine the fields to create a "documents" for TF-IDF (Assuming your feature columns are cleaned of any NA values)
df['documents'] = df['title'] + ' ' + df['authors'] + ' ' + df['subjects'] + ' ' + df['bookshelves']

vectorizer = TfidfVectorizer()
document_vectors = vectorizer.fit_transform(df['documents'])

# Compute the cosine similarity matrix
cosine_sim = linear_kernel(document_vectors, document_vectors)

# Get the pairwsie similarity scores of all books with that book
sim_scores = list(enumerate(cosine_sim[book_index]))

# Sort the books based on the similarity scores
sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

# Preview the data
print(df.head())
print(df.info())