let map;
let latitude = 41;
let longitude = 5;
let elevation = 0;
let markers = [];
let previous = [];
let delay_ns = 5000;
let map_zoom = 5;
let vectorSource = [];

var newPoint = null;
var lastPoint = null;
var marker = null;
var line = null;
var infowindow = null;
var icon = null;
var vectorLayer = null;



var tooltip_data = "<div> <b>Latitude: </b> ".concat(latitude.toFixed(4)) + "<br><b>Longitude: </b>".concat(longitude.toFixed(4)) + "<br><b>Elevation: </b>".concat(elevation) + "</div>";


function initMap() {
    
    marker = new ol.Feature({
        geometry: new ol.geom.Point(ol.proj.transform([longitude, latitude], 'EPSG:4326', 'EPSG:3857')),
        name: 'Enxaneta',
        Alçada: elevation
    });
    
   markers.push(marker);

   vectorSource = new ol.source.Vector({
        features: markers //add  an array of features
    });
   
   var iconStyle = new ol.style.Style({
        image: new ol.style.Icon(/** @type {olx.style.IconOptions} */ ({
        anchor: [0.5, 46],
        anchorXUnits: 'fraction',
        anchorYUnits: 'pixels',
        opacity: 0.75,
        scale: 0.35,
        src: 'static/enxaneta.png'
        }))
    });


    vectorLayer = new ol.layer.Vector({
        source: vectorSource,
        style: iconStyle
    });
    
    
    var map = new ol.Map({
        target: 'map',
        layers: [
          new ol.layer.Tile({
            source: new ol.source.OSM()
          }), vectorLayer
        ],
        view: new ol.View({
          center: ol.proj.fromLonLat([longitude, latitude]),
          zoom: 6
        })
      });
    
    update();
}


function update() {
    updateCoords();

    var newpoint = new ol.geom.Point(ol.proj.transform([longitude, latitude], 'EPSG:4326', 'EPSG:3857'))
    markers[0].setGeometry(newpoint);
    vectorLayer.getSource().changed();
    
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
