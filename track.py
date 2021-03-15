#!/bin/python3
#
# Example from https://rhodesmill.org/skyfield/earth-satellites.html
# 
# Data from https://celestrak.com/satcat/tle.php?INTDES=2020-061
# 1 46292U 20061W   21073.15035660  .00000684  00000-0  45489-4 0  9993
# 2 46292  97.4953 148.5306 0004209  39.0632 321.0901 15.10390241 28942

import sys, webbrowser 
from skyfield.api import load, wgs84
from skyfield.api import EarthSatellite
from datetime import datetime, timedelta, timezone


def decdeg2dms(dd):
    negative = dd < 0
    dd = abs(dd)
    minutes,seconds = divmod(dd*3600,60)
    degrees,minutes = divmod(minutes,60)
    if negative:
        if degrees > 0:
            degrees = -degrees
        elif minutes > 0:
            minutes = -minutes
        else:
            seconds = -seconds
    return (degrees,minutes,seconds)


def getCoords(t):
    geocentric = satellite.at(t)
    subpoint = wgs84.subpoint(geocentric)
    return (subpoint.latitude.degrees, subpoint.longitude.degrees, subpoint.elevation.m)  



ts = load.timescale()

line1 = '1 46292U 20061W   21074.47535270  .00000801  00000-0  52577-4 0  9998'
line2 = '2 46292  97.4950 149.8276 0004086  35.3374 324.8125 15.10393027 29141'




satellite = EarthSatellite(line1, line2, '3CAT-5A', ts)
print(satellite)


# Calculate position at t = now
[lat,log, ele] = getCoords(ts.now())
map_string = '' + str(lat) + ',' + str(log)
print(map_string)
print('Elevation (km):', ele/1000)  
webbrowser.open('https://www.google.com/maps/place/' + map_string) 


#show position in openstreetmap
map_string = 'mlat=' + str(lat)+ '&mlon=' + str(log) + '&zoom=7&layers=N'
print(map_string)
webbrowser.open('http://www.openstreetmap.org/?' + map_string)

# Calculate position at t = now + 5 minutes
step = timedelta(minutes = 5)
t = ts.from_datetime(datetime.now(timezone.utc) + step)
[lat1h,log1h, ele1h] = getCoords(t)
map_string = '' + str(lat1h) + ',' + str(log1h)
print(map_string)
print('Elevation (km):', ele/1000)
#webbrowser.open('https://www.google.com/maps/place/' + map_string)


# Calculate position at t = now + 95.3 minutes
step = timedelta(minutes = 95.3) #, seconds=18)
t = ts.from_datetime(datetime.now(timezone.utc) + step)
[lat1h,log1h,ele1h] = getCoords(t)
map_string = '' + str(lat1h) + ',' + str(log1h)
print(map_string)
print('Elevation (km):', ele/1000)
