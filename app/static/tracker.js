let map;
let la = 41;
let lo = 1;
let markers = [];
let previous = [];
let delay_ns = 5000;
let map_zoom = 8;

function addMarker(location) {
    const marker = new google.maps.Marker({
        position: location,
        map: map,
    });
    markers.push(marker);

}



function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: la, lng: lo },
        zoom: map_zoom,
    });
}

function updateMap(la, lo) {
    map.setCenter(new google.maps.LatLng(la, lo));



    if (markers.length > 0) {
        var previous = markers.slice(-1).pop()
        previous.setMap(null);
    }

    addMarker(new google.maps.LatLng(la, lo));
}
var intervalId = window.setInterval(function() {
    /// call your function here
    lo2 = lo
    lo = lo + 1;

    updateMap(la, lo);

    var line = new google.maps.Polyline({
        path: [new google.maps.LatLng(la, lo), new google.maps.LatLng(la, lo2)],
        strokeColor: "#FF0000",
        strokeOpacity: 1.0,
        strokeWeight: 1,
        geodesic: true,
        map: map
    });
}, delay_ns);