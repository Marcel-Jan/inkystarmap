""" Modules for time and location calculations.
"""
from datetime import datetime, timedelta
import requests
from astral import LocationInfo
from astral.sun import sun

# Default default location: Gouda, The Netherlands
# If IP lookup fails, you're in Gouda!
LAT = 52.0141616
LON = 4.7158104


def get_location_from_ip():
    """Get latitude, longitude and timezone from IP address."""
    try:
        geo = requests.get("https://ipinfo.io/json").json()
        loc = geo["loc"].split(",")  # "52.3676,4.9041"
        lat, lon = float(loc[0]), float(loc[1])
        tz = geo.get("timezone", "UTC")
        return lat, lon, tz
    except Exception as e:
        print(f"Error getting location from IP: {e}")
        return LAT, LON, "UTC"


def is_nighttime(lat, lon, tz):
    """Determine if it is currently nighttime at the given location."""
    city = LocationInfo("auto", "auto", tz, lat, lon)
    s = sun(city.observer, date=datetime.now())
    now = datetime.now().astimezone()
    return now < s["sunrise"] or now > s["sunset"]


def get_sunset_datetime(lat, lon, tz):
    """Return the datetime of today's sunset at the given location."""
    city = LocationInfo("auto", "auto", tz, lat, lon)
    s = sun(city.observer, date=datetime.now())
    return s["sunset"]


def get_nighttime_datetime(lat, lon, tz):
    """ 
        Return the next whole hour if the sun is down.
        Return the next whole hour after sunset if the sun is up.
    """
    city = LocationInfo("auto", "auto", tz)
    s = sun(city.observer, date=datetime.now())
    now = datetime.now().astimezone()
    if is_nighttime(lat, lon, tz):
        return now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    else:
        # Determine next whole hour after sunset
        sunset = get_sunset_datetime(lat, lon, tz)
        return sunset.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)


# if __name__ == "__main__":
#     lat, lon, tz = get_location_from_ip()
#     print(f"Location: {lat}, {lon} ({tz})")
#     if is_nighttime(lat, lon, tz):
#         print("It is currently nighttime.")
#     else:
#         print("It is currently daytime.")
#     dt = get_nighttime_datetime(lat, lon, tz)
#     print(f"Next suitable datetime for observation: {dt}")
