from dataclasses import replace
from json import dumps
from flask import Flask, render_template
import requests
from dotenv import load_dotenv
import os

# from OSMPythonTools.api import Api
# api = Api()
# way = api.query('way/5887599')
# from OSMPythonTools.overpass import Overpass
# overpass = Overpass()
load_dotenv()

app = Flask(__name__)

def preprocessAddress(address = ""):
    return address.replace(" ", "+").replace("and", "%26")

@app.route("/")
def index():
    # requests.get()
    print(os.getenv("SEARCH_URL").format(preprocessAddress("20th and Folsom Streets")))

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