from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import random

app = Flask(__name__)

def read_file_c(file):
    df = pd.read_csv(file, encoding = 'utf-8')
    return df

movies = pd.read_csv('movieranking/ratings1.csv') 

if "Elo" not in movies.columns:
    movies = movies.drop(columns=["Date", "Year", 'Letterboxd URI'])
    movies["Elo"] = 1000
    movies.sort_values(by="Rating", ascending=False)

def elo_percent(A, B):
    AwP = 1/(1+10**((B-A)/400))
    BwP = 1/(1+10**((A-B)/400))
    return AwP, BwP

def elo_recalibrate(A, B, status):
    FirstWinPerc , secondWinPerc = elo_percent(A, B) 
    EloA = A + 32*(status - FirstWinPerc)
    EloB = B + 32*(status - secondWinPerc)
    return EloA, EloB

def rank_movies(movies):
    
    firstMovie = random.randint(0,len(movies))
    secondMovie = random.randint(0,len(movies))
    if(secondMovie == firstMovie):
        return rank_movies()

    EloA = movies["Elo"][firstMovie]
    EloB = movies["Elo"][secondMovie]

    print(""+movies["Name"][firstMovie]+" (L)   or    "+movies["Name"][secondMovie]+" (R)"+"    (if equal = M)")
    choice = input("your decision: ")

    if(choice == "l" or choice == "L"):
        eloA, eloB = elo_recalibrate(EloA, EloB, 1)
    elif(choice == "r" or choice == "R"):
        eloA, eloB = elo_recalibrate(EloA, EloB, 0)
    elif(choice == "m" or choice == "M"):
        eloA, eloB = elo_recalibrate(EloA, EloB, 0.5)
    elif(choice == "stop"):
        movies.to_csv("movieranking/ratings1.csv", index=False)
        return 
    else:
        print("not valid input")
        return rank_movies(movies) 

    movies["Elo"][firstMovie] = eloA
    movies["Elo"][secondMovie] = eloB

    movies = movies.sort_values(by=["Elo"], ascending=False)
    movies.to_csv("movieranking/ratings1.csv", index=False)
    return rank_movies(movies)

def get_movie_cover(movie_name):
    # Use requests to send a GET request to the Letterboxd search page with the movie name
    soup = BeautifulSoup(requests.get(f'https://letterboxd.com/film/{movie_name}/').content, 'html.parser')
    # Find the first movie in the search results
    
    script_w_data = soup.select_one('script[type="application/ld+json"]')
    json_obj = json.loads(script_w_data.text.split(' */')[1].split('/* ]]>')[0])
    return json_obj['image']

# movieA = get_movie_cover(str(movies["Name"][firstMovie]).replace(": ", "-").replace(" ", "-").lower())
# movieB = get_movie_cover(str(movies["Name"][secondMovie]).replace(": ", "-").replace(" ", "-").lower())

# Example usage
cover_url = get_movie_cover(str(movies["Name"][320]).replace(": ", "-").replace(" ", "-").lower())
if cover_url:
    print(f'The cover URL for Inception is {cover_url}')
else:
    print('Could not find a cover for the movie')


@app.route('/', methods=['GET', 'POST'])
def index():
    global movies
    if request.method == 'POST':
        choice = request.form['choice']
        firstMovie = int(request.form['firstMovie'])
        secondMovie = int(request.form['secondMovie'])

        EloA = movies["Elo"][firstMovie]
        EloB = movies["Elo"][secondMovie]

        if choice == "left":
            eloA, eloB = elo_recalibrate(EloA, EloB, 1)
        elif choice == "right":
            eloA, eloB = elo_recalibrate(EloA, EloB, 0)
        elif choice == "middle":
            eloA, eloB = elo_recalibrate(EloA, EloB, 0.5)

        movies["Elo"][firstMovie] = eloA
        movies["Elo"][secondMovie] = eloB

        movies = movies.sort_values(by=["Elo"], ascending=False)
        movies.to_csv("movieranking/ratings1.csv", index=False)

    firstMovie = random.randint(0,len(movies))
    secondMovie = random.randint(0,len(movies))
    if(secondMovie == firstMovie):
        firstMovie = (firstMovie + 1) % len(movies)

    movieA = get_movie_cover(str(movies["Name"][firstMovie]).replace(": ", "-").replace(" ", "-").lower())
    movieB = get_movie_cover(str(movies["Name"][secondMovie]).replace(": ", "-").replace(" ", "-").lower())

    return render_template('index.html', firstMovie=firstMovie, secondMovie=secondMovie, movieA=movieA, movieB=movieB)


if __name__ == "__main__":
    app.run(debug=True)
