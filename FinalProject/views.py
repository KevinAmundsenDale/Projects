from flask import Blueprint, render_template, request, redirect, url_for, send_from_directory, flash, current_app
from werkzeug.utils import secure_filename
from bs4 import BeautifulSoup
import os
import pandas as pd
import requests
import json
import random
import time
from concurrent.futures import ThreadPoolExecutor

views = Blueprint(__name__, "views")

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# movies = pd.read_csv('FinalProject/ratings12.csv') 

def get_movie_data(movie_name):
    # Use requests to send a GET request to the Letterboxd search page with the movie name
    soup = BeautifulSoup(requests.get(f'{movie_name}/').content, 'html.parser')
    # Find the first movie in the search results
    script_w_data = soup.select_one('script[type="application/ld+json"]')
    json_obj = json.loads(script_w_data.text.split(' */')[1].split('/* ]]>')[0])
    cover = json_obj['image'].replace("230", "460").replace("345", "690")

    trailer_tag = soup.find('a', attrs={"data-track-category": "Trailer"})
    trailer = trailer_tag['href'] if trailer_tag else None
    return cover, trailer

def fetch_data(movie_name):
    cover, trailer = get_movie_data(str(movie_name).split(',', 1)[0])
    return cover, trailer

@views.route("/elo")
def home():
    clicked_movie = request.args.get('clicked_index', type=int)
    not_clicked_movie = request.args.get('not_clicked_index', type=int)
    even_match = request.args.get('even_match', type=str) == 'true'
    global movies

        # Select two random movie indices
    movie1 = random.randint(0, len(movies))
    movie2 = random.randint(0, len(movies))
    while movie1 == movie2:  # Ensure they are different
        movie2 = random.randint(0, len(movies) - 1)

    # cover_url = get_movie_cover(str(movies["Letterboxd URI"][movie1]).split(',', 1)[0])
    # cover_url1 = get_movie_cover(str(movies["Letterboxd URI"][movie2]).split(',', 1)[0])

    cover_url = movies["poster"][movie1]
    cover_url1 = movies["poster"][movie2]

    def elo_percent(A, B):
        AwP = 1/(1+10**((B-A)/400))
        BwP = 1/(1+10**((A-B)/400))
        return AwP, BwP

    def elo_recalibrate(A, B, status): 
        FirstWinPerc , secondWinPerc = elo_percent(A, B) 
        EloA = A + 32*(status - FirstWinPerc)
        EloB = B + 32*(abs(status-1) - secondWinPerc)
        return EloA, EloB

    if clicked_movie is not None:
    
        EloA = movies["Elo"][clicked_movie]
        EloB = movies["Elo"][not_clicked_movie]

        eloA, eloB = EloA, EloB

        if even_match:
            eloA, eloB = elo_recalibrate(EloA, EloB, 0.5)
        else:
            eloA, eloB = elo_recalibrate(EloA, EloB, 1)

        movies["Elo"][clicked_movie] = eloA
        movies["Elo"][not_clicked_movie] = eloB

        movies = movies.sort_values(by=["Elo"], ascending=False)
        movies.to_csv(filepath, index=False)

        print(movies.loc[:,:])

    return render_template("index.html", cover=cover_url, cover1=cover_url1, index1=movie1, index2=movie2, movie_name1=movies["Name"][movie1], movie_name2=movies["Name"][movie2])



@views.route("/upload", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_folder = current_app.config['UPLOAD_FOLDER']

            # Create the upload folder if it doesn't exist
            os.makedirs(upload_folder, exist_ok=True)

            global filepath
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)

            # Read the uploaded CSV file
            global movies
            movies = pd.read_csv(filepath)

            if "Letterboxd URI" in movies.columns:
                if "Elo" not in movies.columns:
                    movies["Elo"] = 1000
                    movies.sort_values(by="Rating", ascending=False)
                if "poster" not in movies.columns or "trailer" not in movies.columns:
                    with ThreadPoolExecutor() as executor:
                        results = list(executor.map(fetch_data, movies['Letterboxd URI']))
                        movies['poster'], movies['trailer'] = zip(*results)
                return redirect(url_for('views.home'))
            else:
                render_template('upload.html')
    return render_template('upload.html')