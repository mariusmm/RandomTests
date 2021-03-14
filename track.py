#!/bin/python3
#
# Example from https://rhodesmill.org/skyfielatd/earth-satellites.html
# 
# Data from https://celestrak.com/satcat/tle.php?INTDES=2020-061
# 1 46292U 20061W   21073.15035660  .00000684  00000-0  45489-4 0  9993
# 2 46292  97.4953 148.5306 0004209  39.0632 321.0901 15.10390241 28942

import sys, webbrowser 
from skyfield.api import load, wgs84
from skyfield.api import EarthSatellite

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

ts = load.timescale()

line1 = '1 46292U 20061W   21073.15035660  .00000684  00000-0  45489-4 0  9993'
line2 = '2 46292  97.4953 148.5306 0004209  39.0632 321.0901 15.10390241 28942'

satellite = EarthSatellite(line1, line2, '3CAT-5A', ts)
print(satellite)

t = ts.now()
geocentric = satellite.at(t)
print(geocentric.position.km)

subpoint = wgs84.subpoint(geocentric)
print('Latitude:', subpoint.latitude)
print('Longitude:', subpoint.longitude)
print('Elevation (km):', int(subpoint.elevation.m)/1000)  

[latd,latm,lats] = decdeg2dms(subpoint.latitude.degrees)
[longd, longm, longs] = decdeg2dms(subpoint.longitude.degrees)

if int(latd) > 0:
    NS = 'N'
else:
    NS = 'S'
        
if int(longd) > 0:
    EW = 'E'
else:
    EW = 'W'
    
# Prepare string for google maps
map_string = '' + str(abs(int(latd))) + '°' + str(int(latm)) + '\'' + str(lats) + '\"' + NS + '+' + str(abs(int(longd))) + '°' + str(int(longm)) + '\'' + str(longs) + '\"' + EW

#print(map_string)

webbrowser.open('https://www.google.com/maps/place/' + map_string) 
