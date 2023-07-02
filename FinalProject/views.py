from flask import Blueprint, render_template, request, redirect, url_for
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import random

views = Blueprint(__name__, "views")

def read_file_c(file):
    df = pd.read_csv(file, encoding = 'utf-8')
    return df

movies = pd.read_csv('FinalProject/ratings12.csv') 

def get_movie_cover(movie_name):
    # Use requests to send a GET request to the Letterboxd search page with the movie name
    soup = BeautifulSoup(requests.get(f'{movie_name}/').content, 'html.parser')
    # Find the first movie in the search results
    script_w_data = soup.select_one('script[type="application/ld+json"]')
    json_obj = json.loads(script_w_data.text.split(' */')[1].split('/* ]]>')[0])
    return json_obj['image'].replace("230", "460").replace("345", "690")

cover_url = get_movie_cover(str(movies["Letterboxd URI"][249]).split(',', 1)[0])
cover_url1 = get_movie_cover(str(movies["Letterboxd URI"][32]).split(',', 1)[0])

@views.route("/")
def home():
    return render_template("index.html", cover=cover_url, cover1=cover_url1)