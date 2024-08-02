import pickle
import streamlit as st
import numpy as np

st.header("Book Recommendation System")

# Open files in binary mode
with open('./Models/Book_Recc_Model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('./Models/all_book_name.pkl', 'rb') as book_name_file:
    all_book_name = pickle.load(book_name_file)

with open('./Models/final_ratings.pkl', 'rb') as ratings_file:
    final_ratings = pickle.load(ratings_file)

with open('./Models/book_pivot.pkl', 'rb') as pivot_file:
    book_pivot = pickle.load(pivot_file)


def fetch_poster_urls(suggestion):
    book_name = []
    ids_index = []
    poster_url = []

    for book_id in suggestion[0]:  # Ensure correct indexing
        book_name.append(book_pivot.index[book_id])

    for name in book_name:
        ids = np.where(final_ratings['title'] == name)[0][0]
        ids_index.append(ids)

    for idx in ids_index:
        url = final_ratings.iloc[idx]['image_url']
        poster_url.append(url)

    return poster_url


def recommendation_books(book_name):
    book_list = []
    book_id = np.where(book_pivot.index == book_name)[0][0]
    distance, suggestion = model.kneighbors(book_pivot.iloc[book_id, :].values.reshape(1, -1), n_neighbors=6)

    poster_urls = fetch_poster_urls(suggestion)

    for i in range(1, len(suggestion[0])):  # Start from 1 to avoid the input book itself
        books = book_pivot.index[suggestion[0][i]]
        book_list.append(books)

    return book_list, poster_urls


selected_books = st.selectbox(
    "Type or Select a Book",
    all_book_name
)

if st.button('Recommend Books'):
    if selected_books:
        recommended_books, poster_urls = recommendation_books(selected_books)
        cols = st.columns(len(recommended_books))
        for i, col in enumerate(cols):
            with col:
                st.text(recommended_books[i])
                st.image(poster_urls[i])
