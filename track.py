#!/bin/python3
#
# Example from https://rhodesmill.org/skyfield/earth-satellites.html
# 
# Data from https://celestrak.com/satcat/tle.php?INTDES=2020-061
# 1 46292U 20061W   21073.15035660  .00000684  00000-0  45489-4 0  9993
# 2 46292  97.4953 148.5306 0004209  39.0632 321.0901 15.10390241 28942

import sys, webbrowser 
from skyfield.almanac import dark_twilight_day
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


def visibility(satellite, time, location=None):
    '''
    Say whether the satellite is visible
    '''

    if location is None:
        # Using OAdM ground station location by default
        location = wgs84.latlon(42.05138889, 0.72944444, 1620)

    difference = satellite - location
    topocentric = difference.at(time)
    alt, az, distance = topocentric.altaz()

    eph = load('de421.bsp')
    sunlit = satellite.at(time).is_sunlit(eph)

    solar_elevation = dark_twilight_day(eph, location)
    sun = solar_elevation(time)

    if alt.degrees < 0:
        print(f'{satellite.name} is below the horizon')

    elif sun == 4:
        print(f'{satelltie.name} is above the horizon during day time')

    elif not sunlit:
        print(f'{satellite.name} is above the horizon, but in Earth shadow')

    elif sun > 0:
        print(f'{satellite.name} is above the horizon, during twilight')

    else:
        print(f'{satellite.name} is visible in the night sky!')

    print('Azimuth:', az, 'Elevation:', alt, f'Distance (km): {distance.km:.1f}')


#line1 = '1 46292U 20061W   21074.47535270  .00000801  00000-0  52577-4 0  9998'
#line2 = '2 46292  97.4950 149.8276 0004086  35.3374 324.8125 15.10393027 29141'
#satellite = EarthSatellite(line1, line2, '3CAT-5A', ts)

ts = load.timescale()

# Satellite ID 
n = 46292
url = 'https://celestrak.com/satcat/tle.php?CATNR={}'.format(n)
filename = 'tle-CATNR-{}.txt'.format(n)
satellites = load.tle_file(url, filename=filename, reload=False)
print(satellites)
print(satellites[0].epoch.utc_jpl())

sat_epoch = satellites[0].epoch

# If TLE data is too old, try to update it
if abs(sat_epoch - ts.now()) > 14:
        satellites = load.tle_file(url, filename=filename, reload=True)

satellite = satellites[0]

# Testing output of create_tle
# satellite = EarthSatellite(*create_tle(), ts)

# Calculate position at t = now

now = ts.now()
[lat,log, ele] = getCoords(now)
map_string = '' + str(lat) + ',' + str(log)
print(map_string)
print('Elevation (km):', ele/1000)  
visibility(satellite, now)
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


