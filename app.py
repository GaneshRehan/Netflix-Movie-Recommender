import streamlit as st
import pandas as pd
import pickle
import requests


def fetch_poster(movie_id):
	response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
	data = response.json()
	return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']
	
def recommend(movie):
	movie_index = movies[movies['title'] == movie].index[0]
	distances = similarity[movie_index]
	movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])
	recomended_movies = []
	recomended_movie_posters = []
	counter = 0

	for i in movies_list:
		movie_id = movies.iloc[i[0]].movie_id
		recomended_movies.append(movies.iloc[i[0]].title)
		recomended_movie_posters.append(fetch_poster(movie_id))
		counter += 1
		if counter == 25:
            		break
	return recomended_movies, recomended_movie_posters
		


movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.set_page_config(layout="wide")

title = "Find Your Film"
st.markdown(f'<h1 style="text-align:center;">{title}</h1>', unsafe_allow_html=True)

st.markdown("""
<style>
    .st-cj {

        height: 20px;
    }
    .st-cj select{
        font-size: 40px;
    }
</style>
""", unsafe_allow_html=True)


selected_movie_name = st.selectbox(
'Search...', 
movies['title'].values
        )

if st.button("Search"):
	names, posters = recommend(selected_movie_name)
	cols = st.columns(5)
	image_margin = 100
	for i , name in enumerate(names):
		with cols[i%5]:
			st.image(posters[i])
			st.text(names[i])
			st.markdown(f"""<style>
				div.stImage > img {{
		                margin: {image_margin}px;
		                max-width: 100%;
		                height: auto;
		            }}
		            </style>""",
		            unsafe_allow_html=True,
			)
			
	
	
	
