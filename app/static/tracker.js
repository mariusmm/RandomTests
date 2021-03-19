let map;
let latitude = 0;
let longitude = 0;
let elevation = 0;
let markers = [];
let previous = [];
let delay_ns = 5000;
let map_zoom = 5;

var newPoint = null;
var lastPoint = null;
var marker = null;
var line = null;
var infowindow = null;
var icon = null;

var tooltip_data = "<div> <b>Latitude: </b> ".concat(latitude.toFixed(4)) + "<br><b>Longitude: </b>".concat(longitude.toFixed(4)) + "<br><b>Elevation: </b>".concat(elevation) + "</div>";


function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: latitude, lng: longitude },
        zoom: map_zoom,
    });
    icon = {
        url: "static/enxaneta.png",
        scaledSize: new google.maps.Size(80, 80),
        anchor: new google.maps.Point(40, 40),
    };
    update();
}


function update() {
    updateCoords();
    var newPoint = new google.maps.LatLng(latitude, longitude);
    if (marker) {
        marker.setPosition(newPoint);
    } else {

    marker = new google.maps.Marker({
        icon: icon,
        position: newPoint,
        map: map
    });
    }
    infowindow = new google.maps.InfoWindow({
        content: tooltip_data,
    });
    marker.addListener("mouseover", () => {
        infowindow.open(map, marker);
    });
    marker.addListener('mouseout', function() {
        infowindow.close();
    });

    if (line) {
        line = new google.maps.Polyline({
            path: [newPoint, lastPoint],
            strokeColor: "#FF0000",
            strokeOpacity: 1.0,
            strokeWeight: 1,
            geodesic: true,
            map: map
    });
    } else {
        console.log(latitude);
        line = new google.maps.Polyline({
            path: [newPoint, lastPoint], 
            strokeColor: "#FF0000",
            strokeOpacity: 1.0,
            strokeWeight: 1,
            geodesic: true,
            map: map
        });
    }

    map.setCenter(newPoint);
    
    lastPoint = newPoint;
    
    setTimeout(update, delay_ns);
}

function updateCoords() {
    $.ajax({
        type: "Get",
        cache: false,
        url: "static/satellites.json",
        dataType: "json",
        success: function(data) {
            console.log(data['satellites'][0]);
            latitude = data['satellites'][0]['lat'];
            longitude = data['satellites'][0]['long'];
            elevation = data['satellites'][0]['elevation'];
            tooltip_data = "<div> <b>Latitude: </b> ".concat(latitude.toFixed(4)) + "<br><b>Longitude: </b>".concat(longitude.toFixed(4)) + "<br><b>Elevation: </b>".concat(elevation) + "</div>";
        },
            error: function() {
            alert("There was a problem with the server. Try again soon!");
        }
    });

}