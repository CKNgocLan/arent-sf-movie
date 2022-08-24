'''
A Web application that shows Google Maps around schools, using
the Flask framework, and the Google Maps API.
'''

from flask import Flask, render_template, abort
import requests
from dotenv import load_dotenv
import os

# from OSMPythonTools.api import Api
# api = Api()
# way = api.query('way/5887599')
from OSMPythonTools.overpass import Overpass
overpass = Overpass()
load_dotenv()


app = Flask(__name__)

@app.route("/")
def index():
    result = overpass.query('way["name"="20th and Folsom Streets"]; out body;')
    print(result)
    # stephansdom = result.elements()[0]
    # print(stephansdom.tag('name:en'))
    
    return render_template('index.html',
    )
    # return render_template('index.html', schools=schools)

if __name__ == '__main__':
    app.run(debug = True)