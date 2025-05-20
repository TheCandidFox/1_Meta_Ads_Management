# Designed to use MapBox to find a Isochrone to develop the area in which to advertise from a given point on mappip install requests geopy
import requests
from geopy.geocoders import Nominatim

MAPBOX_ACCESS_TOKEN = 'pk.eyJ1IjoiZHluYW1pY2ZveDIzIiwiYSI6ImNtYXQ0d2kxMDBzdm0ybnB5NWM2dmg3d20ifQ.dWdF5b8hDP5PNoHE5Wkg5g'

def get_coordinates(address):
    geolocator = Nominatim(user_agent="isochrone_locator")
    location = geolocator.geocode(address)
    if location:
        return location.longitude, location.latitude
    else:
        raise Exception("Address not found")

def get_isochrone(lon, lat, minutes=25):
    url = f"https://api.mapbox.com/isochrone/v1/mapbox/driving/{lon},{lat}"
    params = {
        "contours_minutes": minutes,
        "polygons": "true",
        "access_token": MAPBOX_ACCESS_TOKEN,
        "denoise": 1,
        "generalize": 100  # Helps reduce vertices, tweak this
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

# Example usage:
if __name__ == "__main__":
    address = "1600 Amphitheatre Parkway, Mountain View, CA"
    lon, lat = get_coordinates(address)
    isochrone_geojson = get_isochrone(lon, lat, minutes=25)

    # Save GeoJSON to file
    with open("isochrone_25min.geojson", "w") as f:
        import json
        json.dump(isochrone_geojson, f, indent=2)

    print("Isochrone saved as isochrone_25min.geojson")
