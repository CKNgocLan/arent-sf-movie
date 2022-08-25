
# grequests
# import grequests

from datetime import datetime
from re import search
from urllib import response
from urllib.parse import urlencode

from dataclasses import replace
from json import dumps
from flask import Flask, render_template
import requests
from dotenv import load_dotenv
import os

# pandas
import pandas as pd

load_dotenv()

app = Flask(__name__)

# Read CSV file
df = pd.read_csv('Film_Locations_in_San_Francisco.csv')
search_url = os.getenv("SEARCH_URL")

def preprocessAddress(address = ""):
    result = address.lower().replace(" ", "+").replace('streets', 'st')#.replace("and", ", ")
    return result

def getCoordinate(location):
    response = requests.get(url=search_url, params={
        "q": preprocessAddress(location),
        "limit": 1,
        "format": "jsonv2"
    })
    # print(response.json())

    response.close()
    pass

@app.route("/")
def index():
    start=datetime.now()
    for index, row in df.head(10).iterrows():
        if pd.isnull(row['Locations']):
            continue
        
        getCoordinate(preprocessAddress(row["Locations"]))

        # url = "{}?{}".format(search_url, urlencode({
        #     "q": preprocessAddress(row['Locations']),
        #     "limit": 1,
        #     "format": "jsonv2"
        # }))
        # response = requests.get(url)
        # print(response)

        # response.close()
    print("Run time: {}".format(datetime.now() - start))

    # url_list = list(map(lambda cell_value: "{}?{}".format(search_url, urlencode({
    #     "q": cell_value,
    #     "limit": 1,
    #     "format": "jsonv2"
    # })), df.head(1)['Locations'].values))

    # for url in url_list:
    #     response = requests.get(url)
    #     print(response.json())
    #     response.close()

    return render_template('index.html'
        , sf_coor = os.getenv("SF_COORDINATE")
        , title_layer_url_template = os.getenv("TITLE_LAYER_URL_TEMPLATE")
        , title_layer_options = dumps({
            'maxZoom': 50,
            'attribution': '© OpenStreetMap'
        })
    )
    # return render_template('index.html', schools=schools)

if __name__ == '__main__':
    app.run(debug = True)