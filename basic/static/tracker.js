let map;
let latitude = 0;
let longitude = 0;
let elevation = 0;
let markers = [];
let previous = [];
let delay_ns = 5000;
let map_zoom = 5;
let vectorSource = [];
let orbitpoints = [];

var newPoint = null;
var lastPoint = null;
var marker = null;
var line = null;
var infowindow = null;
var icon = null;
var vectorLayer = null;

var orbitLine  = null;
var vectorOrbitLayer = null;


let popup;
var popupOverlay;
var element = document.getElementById('popup');



function initMap() {

    lastPoint = new ol.geom.Point(ol.proj.transform([longitude, latitude], 'EPSG:4326', 'EPSG:3857'));
    marker = new ol.Feature({
        geometry: lastPoint,
        name: 'Enxaneta',
        Alçada: elevation
    });
    
   markers.push(marker);

   vectorSource = new ol.source.Vector({
        features: markers //add  an array of features
    });
   
   var iconStyle = new ol.style.Style({
        image: new ol.style.Icon(/** @type {olx.style.IconOptions} */ ({
        anchor: [0.5, 0.7],
        anchorXUnits: 'fraction',
        anchorYUnits: 'fraction',
        opacity: 0.75,
        scale: 0.35,
        src: 'static/enxaneta.png'
        }))
    });


    vectorLayer = new ol.layer.Vector({
        source: vectorSource,
        style: iconStyle
    });
   
    map = new ol.Map({
        target: 'map',
        layers: [
          new ol.layer.Tile({
            source: new ol.source.OSM()
             }), vectorLayer
        ],
        view: new ol.View({
          center: ol.proj.fromLonLat([longitude, latitude]),
          zoom: 5
        })
      });
     
    update();
}


function update() {
    updateCoords();

    newPoint = new ol.geom.Point(ol.proj.transform([longitude, latitude], 'EPSG:4326', 'EPSG:3857'))
    markers[0].setGeometry(newPoint);
    vectorLayer.getSource().changed();
    
    if (longitude < 0)
       longitude = longitude + 360;
    
    if (longitude != 0 && latitude != 0)
        orbitpoints.push([longitude, latitude]);
    
    
    // Limit array of points to 1500 that should be ~1.5 orbits
    orbitpoints = orbitpoints.slice(-1500);
        
    // Remove old layer, we will create a new one
    map.removeLayer(vectorOrbitLayer);
    
    orbitLine = new ol.Feature({
        geometry: new ol.geom.LineString(orbitpoints).transform('EPSG:4326', 'EPSG:3857')
    });
    
    var vectorOrbit = new ol.source.Vector({});
    vectorOrbit.addFeature(orbitLine);
    
    vectorOrbitLayer = new ol.layer.Vector({
        source: vectorOrbit,
        style: new ol.style.Style({
            fill: new ol.style.Fill({ color: '#FF0000', weight: 4 }),
            stroke: new ol.style.Stroke({ color: '#FF0000', width: 2 })
        })
    });
    
    map.addLayer(vectorOrbitLayer);
   
    vectorOrbitLayer.getSource().changed();


    var popup = new ol.Overlay({
        element: document.getElementById('popup')
      });
      map.addOverlay(popup);
    
      map.on('singleclick', function(evt) {
        var feature = map.forEachFeatureAtPixel(evt.pixel, function(feat, layer) {
          return feat;
        });
        var element = $(popup.getElement());
        element.popover('destroy');
        if (feature) {   
            popup.setPosition(evt.coordinate);
            element.popover({
              'placement': 'top',
              'animation': false,
              'html': true,
              'title': '<h1> Enxaneta </h1>',
              'content':  "<div class='sat'> <b>Latitud: </b> ".concat(latitude.toFixed(4)) + " &#176<br><b>Longitud: </b>".concat(longitude.toFixed(4)) + " &#176<br><b>Altura: </b>".concat((elevation/1000).toFixed(0)) + " km</div>"
            }).popover('show');
        }
      });
      map.on('pointermove', function(evt) {
        map.getTargetElement().style.cursor = map.hasFeatureAtPixel(evt.pixel) ? 'pointer' : '';
      })
    map.getView().setCenter(ol.proj.transform([longitude, latitude], 'EPSG:4326', 'EPSG:3857'))
    setTimeout(update, delay_ns);
}

function updateCoords() {
    $.ajax({
        type: "Get",
        cache: false,
        url: "static/satellites.json",
        dataType: "json",
        success: function(data) {
            // console.log(data['satellites'][0]);
            latitude = data['satellites'][0]['lat'];
            longitude = data['satellites'][0]['long'];
            elevation = data['satellites'][0]['elevation'];
        },
            error: function() {
            alert("There was a problem with the server. Try again soon!");
        }
    });

}
