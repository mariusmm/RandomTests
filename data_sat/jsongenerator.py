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
        "nextpass": 1616710596,
        "points": 
        [
            {"lat": -66.56194897413042, "long": -66.28465777505991, "elevation": 568203, "date:" : 1616690203},
            {"lat": -62.99833496728054, "long": -69.25044313228865, "elevation": 567927, "date:" : 1616690263},
            ...
            {}
        ]
    }
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



if __name__ == '__main__':
    sleep_time = 5
    print("Updating data every", sleep_time, "seconds")
    
    ts = load.timescale()
    
    ## Preliminary TLE from OC
    #line1 = '1 00000U 00000A   21082.43671296  .00000000  00000-0  15378-4 0  08'
    #line2 = '2 00000  97.5663 343.3505 0020543 246.5020 55.8365  15.05249025 09'
    
    ## Updated TLE at 19:00 from OC
    #line1 = '1 00000U 00000A   21081.43671296  .00000000  00000-0  15068-4 0  07'
    #line2 = '2 00000  97.5665 345.3219 0020543 246.5023 55.8363  15.05248993 09'
    
    ## Updated TLE 27 March, NORDAN id seems to be: 2021-022Y
    #line1 = '1 47954U 21022Y   21086.12491909 -.00000062  00000-0  00000+0 0  9996'
    #line2 = '2 47954  97.5672 349.9056 0020226 227.5117 270.1182 15.05637633   381'
    
    ## Updated to 29 March
    #line1 = '1 47954U 21022Y   21088.04778777 -.00000062  00000-0  00000+0 0  9990'
    #line2 = '2 47954  97.5677 351.7944 0020601 219.0280 254.5914 15.05638547   673'
    
    ## Updated to 13 April
    #line1 = '1 47954U 21022Y   21103.11279148  .00000235  00000-0  20485-4 0  9999'
    #line2 = '2 47954  97.5649   6.5691 0021842 168.9912 191.1797 15.05669275  2947'
    
    #satellite = EarthSatellite(line1, line2, '3CAT-5A', ts)
    
    ## When observational TLE are publised, use the following lines 
    
    # Satellite ID 
    sats = [47961, 25544]
    satellites = dict()
    for n in sats:
        url = 'https://celestrak.com/NORAD/elements/gp.php?CATNR={}'.format(n)
        filename = 'tle-CATNR-{}.txt'.format(n)
        satellites[n] = load.tle_file(url, filename=filename, reload=False)

    last_try = ts.now()
    
    # Calculate position at t = now
    #location = wgs84.latlon(42.05138889, 0.72944444, 1620);
    location = wgs84.latlon(41.726389, 1.829167, 238);
        
    while True:
        
        f = open ('/home/tracker/app/resources/satellites.json','w')
        json_data = "{\"satellites\":["
        for n in satellites:
            # If TLE data is too old, try to update it
            # Difference between epoch times are in days
            if abs(satellites[n][0].epoch - ts.now()) > 5:
                 if abs(ts.now() - last_try) > 1:
                     url = 'https://celestrak.com/NORAD/elements/gp.php?CATNR={}'.format(n)
                     filename = 'tle-CATNR-{}.txt'.format(n)
                     print("reloading TLE file: " + filename)
                     satellites[n] = load.tle_file(url, filename=filename, reload=True)
                     last_try = ts.now()
        
            satellite = satellites[n][0]
            margin = timedelta(days = 1);
            t = ts.from_datetime(datetime.now(timezone.utc) + margin);
            # When the satellite will be visible from Manresa at 20º
            passes = satellite.find_events(location, ts.now(), t, 20);

            if (passes[1][0] == 0):
                 nextpass = int(passes[0][0].utc_datetime().timestamp());

            json_data += "{\"id\": " + str(n)
            json_data += ",\"nextpass\": " + str(nextpass);
            json_data += ",\"points\": [";
            
            # Iterate to compute 95 points, completing ~1 orbit
            for x in range (95):
                step = timedelta(minutes = x)
                t = ts.from_datetime(datetime.now(timezone.utc) + step)
                [lat, log, ele] = getCoords(satellite, t)
                map_string = '' + str(lat) + ', ' + str(log)
                json_data += "{\"lat\": "  + str(lat) + ", \"long\": " + str(log) + ", \"elevation\": " + str(int(ele)) + ", \"date:\" : " + str(int(t.utc_datetime().timestamp())) + "},"
            # End of a satellite
            json_data += "{}]},\r\n"

        # End of the file
        json_data += "{}]}\r\n"

        f.write(json_data)
        f.close()
        time.sleep(sleep_time)
    
