import numpy as np
import astropy.units as u
from astropy.time import Time
import astropy.constants as cnt


def time_from_date(epoch):
    """
    Compute TLE ephemeris time from ISO datetime string

    :param epoch: epoch in ISO format
    :param epoch: str

    :return: epoch in TLE format
    :rtype: str
    """

    in_time = Time(epoch)
    yday = in_time.yday.split(":")

    year = f"{int(yday[0])}"
    day = yday[1]

    day_time = in_time.datetime.time()
    day_hours = day_time.hour + day_time.minute/60 + day_time.second/3600
    day_frac = f"{day_hours/24:.8f}"

    return f"{year[-2:]}{day}{day_frac[1:]}"
    

def checksum(line): 
    """
    Compute last digit on line 1 and 2

    :param line: line to compute the checksum, excluding last digit
    :type line: str

    :return: checksum modulo 10
    :rtype: int
    """

    total = 0 
    for digit in line: 
        total += int(digit) if digit.isdigit() else 0 
        total += 1 if digit == "-" else 0 
    return str(total % 10)


def mean_anomaly(true_anomaly, eccentricity):
    """
    Compute mean anomaly from true anomaly and eccentricity

    :param true_anomaly: true anomaly in degrees
    :type true_anomaly: float
    :param eccentricity: eccentricity
    :type eccentricity: float

    :return: mean anomaly in degrees
    :rtype: float
    """

    cos_nu = np.cos(true_anomaly * np.pi / 180)

    cos_e = (cos_nu + eccentricity) / (1 + eccentricity * cos_nu)

    eccentric = np.arccos(cos_e)
    mean = eccentric - eccentricity * np.sin(eccentric)

    return f"{mean * 180 / np.pi:9.4f}"


def mean_motion(semi_major):
    """
    Compute the mean daily motion from the semi_major axis

    :param semi_major: semi-major axis of the orbit in meters
    :type semi_major: float

    :return: mean daily motion in revolutoins per day
    :rtype: float
    """

    period = 2 * np.pi * (semi_major * u.m)**1.5 / np.sqrt(cnt.G * cnt.M_earth)

    return f"{1/period.to(u.day).value:12.8f}"


def create_tle():
    """
    Compute TLE for ENXANETA from the orbital elements

    Expected output:

    ENXANETA
    1 00000U 21000AAA 21080.43671296 0.00000000 000000-0  00000-0 0    05
    2 00000  97.5700 345.9492 0017590 182.3600 119.9155 15.07648827    07
    """

    orbital_elements = dict(DATE="2021-03-21T10:28:52.000",
                            SEMIMAJOR_AXIS_MET=6921523.482821434,
                            ECCENTRICITY=0.001759,
                            INCLINATION_DEG=97.57,
                            RAAN_DEG=-14.050813373007466,
                            W_DEG=182.36,
                            TA_DEG=120.09)

    line_zero = "ENXANETA"

    line_one = "1 00000U 21000AAA "
    line_one += time_from_date(orbital_elements["DATE"])
    line_one += " +.00000000 000000-0  00000-0 0    0"
    line_one += checksum(line_one)

    inclination = orbital_elements["INCLINATION_DEG"]
    node = orbital_elements["RAAN_DEG"]
    node = 360 + node if node < 0 else node
    eccentricity = orbital_elements["ECCENTRICITY"]
    ecc = f"{eccentricity:9.7f}"
    omega = orbital_elements["W_DEG"]
    line_two = f"2 00000  {inclination:7.4f} {node:8.4f} {ecc[2:]} {omega:8.4f}"
    line_two += mean_anomaly(orbital_elements["TA_DEG"], eccentricity)
    line_two += mean_motion(orbital_elements["SEMIMAJOR_AXIS_MET"])
    line_two += "    0"
    line_two += checksum(line_two) 

    print(line_zero)
    print(line_one)
    print(line_two)

    return line_one, line_two, line_zero


if __name__ == "__main__":
    create_tle()
