#!/bin/python3
#
# Data from https://celestrak.com/satcat/tle.php?INTDES=2020-061
# 
# Generates a JSON file for the webserver:
# JSON format
# 
'''
{
"satellites":
[
  {
    "id": 46292, 
    "lat": -19.977352947359257, 
    "long": 7.00249024881578, 
    "elevation": 540783
  },
  {}
]
}

'''
import os
import time
import sys
from skyfield.almanac import dark_twilight_day
from skyfield.api import load, wgs84
from skyfield.api import EarthSatellite
from datetime import datetime, timedelta, timezone


def getCoords(sat, t):
    geocentric = sat.at(t)
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
        print(f'{satellite.name} is above the horizon during day time')

    elif not sunlit:
        print(f'{satellite.name} is above the horizon, but in Earth shadow')

    elif sun > 0:
        print(f'{satellite.name} is above the horizon, during twilight')

    else:
        print(f'{satellite.name} is visible in the night sky!')

    print('Azimuth:', az, 'Elevation:', alt, f'Distance (km): {distance.km:.1f}')



def run():
    sleep_time = 5
    print("Updating data every", sleep_time, "seconds")
    ts = load.timescale()
    #line1 = '1 46292U 20061W   21074.47535270  .00000801  00000-0  52577-4 0  9998'
    #line2 = '2 46292  97.4950 149.8276 0004086  35.3374 324.8125 15.10393027 29141'
    #satellite = EarthSatellite(line1, line2, '3CAT-5A', ts)

    # Satellite ID 
    n = 46292
    url = 'https://celestrak.com/satcat/tle.php?CATNR={}'.format(n)
    filename = 'tle-CATNR-{}.txt'.format(n)
    satellites = load.tle_file(url, filename=filename, reload=False)
    satellite = satellites[0]
    #print(satellite)
    #print(satellite.epoch.utc_jpl())

    sat_epoch = satellite.epoch
    last_try = ts.utc(2000)

    # If TLE data is too old, try to update it
    if abs(sat_epoch - ts.now()) > 14:
        # If already tried today, skip
        if abs(ts.now() - last_try) > 1:
            satellites = load.tle_file(url, filename=filename, reload=True)
            last_try = ts.now()

    # Calculate position at t = now
    while True:
        # If TLE data is too old, try to update it
        if abs(sat_epoch - ts.now()) > 14:
            if abs(ts.now() - last_try) > 1:
                satellites = load.tle_file(url, filename=filename, reload=True)
                last_try = ts.now()

        now = ts.now()
        [lat,log, ele] = getCoords(satellite, now)
        map_string = '' + str(lat) + ', ' + str(log)
        #print(map_string)
        #print('Elevation (km):', ele/1000)   
        json_data = "{\"satellites\":[{\"id\": " + str(n) + ", \"lat\": "  + str(lat) + ", \"long\": " + str(log) + ", \"elevation\": " + str(int(ele)) + "},"
        json_data += "{}]}\r\n"
        #print (json_data)
        f = open('app/static/satellites.json','w')
        f.write(json_data)
        f.close()
        time.sleep(sleep_time)

