function initMap() {
    const displayMap = new google.maps.Map(document.getElementById('map'), {
        center: new google.maps.LatLng(school.lat, school.lng),
        zoom: 16
      });

    new google.maps.Marker({
        position: new google.maps.LatLng(school.lat, school.lng),
        displayMap,
        title: school.name,
    });
}