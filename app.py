# grequests
import grequests
import requests

from datetime import datetime
from re import search
import string
from urllib import response
from urllib.parse import urlencode
import numpy as np

from dataclasses import replace
from json import dumps
from flask import Flask, render_template, request, jsonify

from dotenv import load_dotenv
import os
from os.path import exists

# pandas
import pandas as pd

load_dotenv()

film_dataset_file = os.getenv('SF_MOVIES_FILE')
coordinate_file = os.getenv('COORDINATES_DATASET')

coor_df_file = 'coor_df.csv'

app = Flask(__name__)


def preprocessAddress(address = ""):
    result = str(address).lower().replace(" ", "+").replace('streets', 'st')
    return "{}, San Francisco".format(result)

def generateCoordinateCsv():
    term_df = pd.read_csv(film_dataset_file)
    search_url = os.getenv("SEARCH_URL")
    urls = list(map(lambda location: "{}?{}".format(search_url, urlencode({
        "q": preprocessAddress(location),
        "limit": 1,
        "format": "jsonv2"
    })), term_df['Locations'].values))

    print("Fetching coordinations...")
    responses = grequests.map((grequests.get(url) for url in urls), size=30)
    print("End of fetching coordinations...")

    json_responses = list(map(lambda response: response.json() if response is not None and response.status_code == 200 else None, responses))

    pd.DataFrame(data={
        'Locations': term_df['Locations'].values,
        'Latitude': [defCoor(js, 'lat') for js in json_responses],
        'Longitude': [defCoor(js, 'lon') for js in json_responses],
    }).to_csv(coor_df_file, mode='w', index=False)
    
    coor_df = pd.read_csv(coor_df_file)

    total_df = term_df.merge(right=coor_df, on='Locations', how='right')

    print("Exporting CSV ...")
    total_df.to_csv(coordinate_file, mode='w', index=False, float_format='%.3f')
    print("Exported {} file".format(coordinate_file))

def defCoor(json_response, dict_key: string):
    if (json_response is not None
        and len(json_response) > 0):
        return json_response[0][dict_key]
    else:
        return np.nan

def getCoordinatesDf(title):
    if title:
        return df[['Title', 'Latitude', 'Longitude']].loc[df['Title'].str.contains(title)].transpose().to_dict()
    else:
        return df[['Locations', 'Latitude', 'Longitude']].loc[~df['Locations'].isnull()].transpose().to_dict()

@app.route("/getLocations", methods=['GET'])
def getLocations():
    movie_title = request.args.get('title')

    coors_dict = getCoordinatesDf(title=movie_title)
    return jsonify(
        locations_dict = dumps(coors_dict)
    )

@app.route("/")
def index():
    global df
    if exists(coordinate_file):
        print('Coordinates CSV file is existing!')
        df = pd.read_csv(coordinate_file)
    else:
        start=datetime.now()
        df = pd.read_csv(film_dataset_file)
        print("Generating CSV file...")
        generateCoordinateCsv()
        print("Generating CSV time: {}".format(datetime.now() - start))

    df = pd.read_csv(coordinate_file)
    df = df[df['Latitude'].notnull()]
    coors_dict = getCoordinatesDf(None)

    return render_template('index.html'
        , sf_coor = os.getenv("SF_COORDINATE")
        , autocomplete_search_source = dumps(list(dict.fromkeys(df['Title'].tolist())))
        , locations_dict = dumps(coors_dict)
    )

if __name__ == '__main__':
    from gevent import monkey
    monkey.patch_all()

    app.run(debug = False)