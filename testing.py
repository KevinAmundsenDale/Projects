from bs4 import BeautifulSoup
import json
import requests

movie = "https://boxd.it/kSz4"

def get_movie_vid(movie_site):
        # Use requests to send a GET request to the Letterboxd search page with the movie name
        soup = BeautifulSoup(requests.get(f'{movie_site}/').content, 'html.parser')
        # Find the first movie in the search results
        trailer_tag = soup.find('a', attrs={"data-track-category": "Trailer"})
        trailer = trailer_tag['href'].rsplit("rel")[0]+"autoplay=1&rel=1"
        print(trailer)
        return 0

get_movie_vid(movie)