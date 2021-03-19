let map;
let la = 41;
let lo = 1;
let elevation = 0;
let markers = [];
let previous = [];
let delay_ns = 5000;
let map_zoom = 8;


var marker = null;
var line = null;
var infowindow = null;
var icon = null;

var tooltip_data = "<div> Lat: ".concat(la)+" Long: ".concat(lo)+" Elevation: ".concat(elevation)+"</div>";



function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: la, lng: lo },
        zoom: map_zoom,
    });
    icon = {
        url: "static/satellite.png", // url
        scaledSize: new google.maps.Size(50, 50), // scaled size
        anchor: new google.maps.Point(25, 25),
    };
    update();
}





function update() {
    var newPoint = new google.maps.LatLng(la, lo);
  


      if (marker) {
        marker.setPosition(newPoint);
      }
      else {

        marker = new google.maps.Marker({
          icon: icon,
          position: newPoint,
          map: map
        });
      }
      tooltip_data = "<div> Lats: ".concat(la)+" Long: ".concat(lo)+" Elevation: ".concat(elevation)+"</div>";
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
        line = new google.maps.Polyline({
            path: [newPoint, newPoint],
            strokeColor: "#FF0000",
            strokeOpacity: 1.0,
            strokeWeight: 1,
            geodesic: true,
            map: map
        });
      }

      map.setCenter(newPoint);

      lastPoint = newPoint;

      lo = lo + 1;


  
  
    // Call the autoUpdate() function every 5 seconds
    setTimeout(update, delay_ns);
  }

  