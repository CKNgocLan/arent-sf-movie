class Movie {
    constructor(title, latitude, longitude) {
        this.title = title;
        this.lat = latitude;
        this.lon = longitude;
    }
}

function initMap(sf_coor, title_layer_url_template, title_layer_options, locations_dict) {
    var map = L.map('map').setView(sf_coor, 12);

    L.tileLayer(title_layer_url_template, JSON.parse(title_layer_options)).addTo(map);

    // L.marker([37.769368099999994, -122.48218371117709]).addTo(map);

    locations = JSON.parse(locations_dict)
    // for(let index = 0; index < 10; index++) {
    //     console.log(locations[index])
    // }
    // locs = locations.map(l => new Movie(l.Title, l.Latitude, l.Longitude))
    loc_entries = Object.entries(locations)//.slice(0, 4)
    // console.log(loc_entries)
    movies = loc_entries.map(l => new Movie(l[1].Title, l[1].Latitude, l[1].Longitude))
    // console.log(`Lat: ${movies[1].lat} - Lon: ${movies[1].lon}`)
    // L.marker([movies[1].lat, movies[1].lon]).addTo(map);
    for(let movie of movies) {
        // console.log([movie.lat, movie.lon])
        L.marker([movie.lat, movie.lon]).addTo(map);
    }

    // l = locations[0]
    // console.log(new Movie(l.Title, l.Latitude, l.Longitude))
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
            if (current.name == $input.val()) {
                matches.push(current.name);
            }
        }
    });

    // console.log('Search Source:')
    // console.log(JSON.parse(coor_df))
}

function showValues(obj) {
    console.log(obj)
}