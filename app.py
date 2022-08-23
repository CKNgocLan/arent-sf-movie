'''
A Web application that shows Google Maps around schools, using
the Flask framework, and the Google Maps API.
'''

from flask import Flask, render_template, abort
# import request
from dotenv import load_dotenv
import os
load_dotenv()


app = Flask(__name__)

class School:
    def __init__(self, key, name, lat, lng):
        self.key  = key
        self.name = name
        self.lat  = lat
        self.lng  = lng

schools = (
    School('hv',      'Happy Valley Elementary',   37.9045286, -122.1445772),
    School('stanley', 'Stanley Middle',            37.8884474, -122.1155922),
    School('wci',     'Walnut Creek Intermediate', 37.9093673, -122.0580063)
)
schools_by_key = {school.key: school for school in schools}

nearby_search_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=-33.8670522%2C151.1957362&radius=1500&type=restaurant&keyword=cruise&key=" + os.getenv("API_KEY")



@app.route("/")
def index():
    school = schools_by_key.get('hv')
    return render_template('index.html',
        school = school,
        map_api = "https://maps.googleapis.com/maps/api/js?key={}-L0&callback=initMap".format(os.getenv("API_KEY"))
    )
    # return render_template('index.html', schools=schools)


@app.route("/<school_code>")
def show_school(school_code):
    # school = schools_by_key.get(school_code)
    school = schools_by_key.get('hv')
    if school:
        return render_template('index.html', school=school)
    else:
        abort(404)

# app.run(host='localhost', debug=True)