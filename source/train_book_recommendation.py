import argparse
import tensorflow as tf
from sklearn.model_selection import train_test_split
import pickle
from tensorflow.keras.layers import TextVectorization
import gc
import numpy as np

# Initiate the parser
parser = argparse.ArgumentParser()
parser.add_argument("--num_books", type=int, help="Number of books", required=True)
args = parser.parse_args()

num_books = args.num_books

# load the processed data
with open('/mnt/d/Main/Uni/bakalauras/BookRecommendation/source/preprocessing/preprocessed_data_chunk_' + str(
        num_books) + '.pkl', 'rb') as f:
    books_encoded, genres_encoded, authors_encoded, vocab = pickle.load(f)

maxlen = 100  # replace this with the actual value or load it along with the other data
vectorizer = TextVectorization(max_tokens=20000, output_sequence_length=maxlen)
vectorizer.set_vocabulary(vocab)


books_encoded_np = np.array(books_encoded)
X_train, X_test, authors_train, authors_test = train_test_split(books_encoded_np, authors_encoded, random_state=42)
_, _, genres_train, genres_test = train_test_split(books_encoded_np, genres_encoded, random_state=42)


del books_encoded
gc.collect()

shared_embedding = tf.keras.layers.Embedding(input_dim=len(vectorizer.get_vocabulary()), output_dim=64, mask_zero=True)
shared_lstm = tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64))
shared_dense = tf.keras.layers.Dense(64, activation='relu')

input_layer = tf.keras.layers.Input(shape=(maxlen,))
x = shared_embedding(input_layer)
x = shared_lstm(x)
x = shared_dense(x)
out_authors = tf.keras.layers.Dense(authors_encoded.shape[1], activation='sigmoid', name='authors')(x)
out_genres = tf.keras.layers.Dense(genres_encoded.shape[1], activation='sigmoid', name='genres')(x)

model = tf.keras.models.Model(inputs=input_layer, outputs=[out_authors, out_genres])

# Compile the model
model.compile(loss={'authors': 'categorical_crossentropy', 'genres': 'categorical_crossentropy'},
              optimizer='adam',
              metrics={'authors': 'accuracy', 'genres': 'accuracy'})

# Train the model
model.fit(X_train, {'authors': authors_train, 'genres': genres_train}, epochs=100)

model.save(f'model/{num_books}.keras')




