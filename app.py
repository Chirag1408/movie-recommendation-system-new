import pickle
import streamlit as st
import requests

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=412d4a92b67f012377a5a9a786c86e75&language=en-US"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return "https://image.tmdb.org/t/p/w500" + data['poster_path']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster for {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=Image+Not+Found"

# def fetch_poster(movie_id):
#      url = "https://api.themoviedb.org/3/movie/{}?api_key=412d4a92b67f012377a5a9a786c86e75".format(movie_id)
#      data = requests.get(url)
#      data = data.json()
#      poster_path = data['poster_path']
#      full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
#      return full_path


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_name = []
    recommended_movie_poster = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_poster.append(fetch_poster(movie_id))
        recommended_movie_name.append(movies.iloc[i[0]].title)

    return recommended_movie_name,recommended_movie_poster

st.title('Movie Recommender')

movies = pickle.load(open('./movie_list_new.pkl','rb'))
similarity = pickle.load(open('./similarity_tfidf.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
