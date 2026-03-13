from geopy.geocoders import Nominatim
from time import sleep

geolocator= Nominatim(user_agent="world_monitor", timeout=10)
geocode_cache= {}

def get_coordinates(location):
    if location in geocode_cache:
        return geocode_cache[location]

    try:
        geo= geolocator.geocode(location)

        sleep(1)

        if geo:
            coords= (geo.latitude, geo.longitude)
            geocode_cache[location]= coords
            return coords

    except Exception as e:
        print("Geocode error:", location, e)

    geocode_cache[location]= (None, None)
    return None, None

def get_country_from_coordinates(lat, lon):
    try:
        result= geolocator.reverse((lat, lon), language="en")

        sleep(1)

        if result and "country" in result.raw["address"]:
            return result.raw["address"]["country"]

    except Exception as e:
        print(f"Reverse geocode error for {lat},{lon}: {e}")

    return "Unknown"