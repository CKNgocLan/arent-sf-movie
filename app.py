
# grequests
# import grequests

from datetime import datetime
from re import search
import string
from urllib import response
from urllib.parse import urlencode
import numpy as np

from dataclasses import replace
from json import dumps
from flask import Flask, render_template

from dotenv import load_dotenv
import os
from os.path import exists

# pandas
import pandas as pd

load_dotenv()

film_dataset_file = 'Film_Locations_in_San_Francisco.csv'
coordinate_file = 'Coordinates.csv'

app = Flask(__name__)

# Read CSV file
df = pd.read_csv(coordinate_file)

def preprocessAddress(address = ""):
    result = address.lower().replace(" ", "+").replace('streets', 'st')#.replace("and", ", ")
    return result

def generateCoordinateCsv(row_number: int):
    term_df = df.head(row_number)
    search_url = os.getenv("SEARCH_URL")
    urls = list(map(lambda location: "{}?{}".format(search_url, urlencode({
        "q": preprocessAddress(location),
        "limit": 1,
        "format": "jsonv2"
    })), term_df['Locations'].values))

    # unsent_responses = (grequests.get(url) for url in urls)
    responses = grequests.map((grequests.get(url) for url in urls), size=30)

    json_responses = list(map(lambda response: response.json() if response.status_code == 200 else None, responses))

    coor_df = pd.DataFrame(data={
        'Locations': term_df['Locations'].values,
        'Latitude': [defCoor(js, 'lat') for js in json_responses],
        'Longitude': [defCoor(js, 'lon') for js in json_responses],
    })
    total_df = df.merge(right=coor_df, on='Locations', how='left')

    print("Exporting CSV ...")
    total_df.to_csv(os.getenv('COORDINATES_DATASET'), float_format='%.3f')
    print("Exported {} file".format(os.getenv('COORDINATES_DATASET')))
    # total_df.to_csv(coor_dataset, float_format='%.3f')
    # print("Exported {} file".format(coor_dataset))

def defCoor(json_response, dict_key: string):
    if (json_response is not None
        and len(json_response) > 0):
        return json_response[0][dict_key]
    else:
        return np.nan

@app.route("/")
def index():

    if exists(os.getenv('COORDINATES_DATASET')):
        print('Having coordinates CSV file')
    else:
        start=datetime.now()
        generateCoordinateCsv(len(df.index))
        print("Generating CSV time: {}".format(datetime.now() - start))

    coors_dictt = df[['Title', 'Latitude', 'Longitude']].transpose().to_dict()

    return render_template('index.html'
        , sf_coor = os.getenv("SF_COORDINATE")
        , title_layer_url_template = os.getenv("TITLE_LAYER_URL_TEMPLATE")
        , title_layer_options = dumps({
            'maxZoom': 50,
            'attribution': '© OpenStreetMap'
        })
        , autocomplete_search_source = dumps(list(dict.fromkeys(df['Title'].tolist())))
        , locations_dict = dumps(coors_dictt)
    )
    # return render_template('index.html', schools=schools)

if __name__ == '__main__':
    app.run(debug = True)