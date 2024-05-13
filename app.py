import pickle
from typing import Any

import pandas as pd
import requests
import streamlit as st


def fetch_poster(id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=b49c61843022483b7b414cfbada4dc5d&language=en-US'.format(id))
    data = response.json()
    print(data)
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies: list[Any] = []
    recommended_movies_posters = []
    for i in movies_list:
        id = movies.iloc[i[0]].id
        # fetch poster from API
        recommended_movies.append(movies.iloc[i[0]].title)

        recommended_movies_posters.append(fetch_poster(id))
    return recommended_movies, recommended_movies_posters


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommendation System')

selected_movie_name = st.selectbox(
    'Lets recommend some interesting movies',
    movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])
