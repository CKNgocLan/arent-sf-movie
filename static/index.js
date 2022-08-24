function initMap(sf_coor, title_layer_url_template, title_layer_options) {
    var map = L.map('map').setView(sf_coor, 12);

    L.tileLayer(title_layer_url_template, JSON.parse(title_layer_options)).addTo(map);

    // var marker =
    L.marker([37.769368099999994, -122.48218371117709])
        .addTo(map);

    // address = "20th and Folsom Streets"
    // uri = `${address}`
    // $.get(location.protocol + '//nominatim.openstreetmap.org/search?format=json&q=' + address, function (data) {
    //     console.log(data);
    // });
}