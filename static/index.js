class Movie {
    constructor(title, latitude, longitude) {
        this.title = title;
        this.lat = latitude;
        this.lon = longitude;
    }
}

var map;

function initMap(sf_coor, locations_dict) {
    this.map = L.map('map').setView(sf_coor, 12);

    L.tileLayer(
        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        {
            'maxZoom': 50,
            'attribution': '© OpenStreetMap'
        }).addTo(map);

    showMarkers(locations_dict)
}

function showMarkers(locations_dict) {
    $(".leaflet-marker-icon").remove(); $(".leaflet-popup").remove();
    $(".leaflet-pane.leaflet-shadow-pane").remove();

    locations = JSON.parse(locations_dict)
    loc_entries = Object.entries(locations)
    movies = loc_entries.map(l => new Movie(l[1].Title, l[1].Latitude, l[1].Longitude))
    for(let movie of movies) {
        L.marker([movie.lat, movie.lon]).addTo(this.map);
    }
}

function addAutoSearchSource(coor_df) {
    // Initializes input( name of states) with a typeahead
    var $input = $(".typeahead");
    $input.typeahead({
        source: JSON.parse(coor_df)
        , autoSelect: true,
    });
    $input.change(function () {
        var current = $input.typeahead("getActive");
        matches = [];

        if (current) {
            // Some item from your input matches with entered data
            if (current == $input.val()) {
                matches.push(current);
            }
        }
        $.get('/getLocations', {'title': $input.val()} , function(response, status) {
            showMarkers(response.locations_dict)
        })
    });
}