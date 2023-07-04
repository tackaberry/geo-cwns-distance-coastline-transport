import googlemaps
from datetime import datetime
import configparser

config = configparser.ConfigParser()
config.read('config.ini')


gmaps = googlemaps.Client(key=config['default']['google_api_key'])

def getStateForLatLon(x):
    result = gmaps.reverse_geocode((x.latitude, x.longitude))
    for component in result[0]['address_components']:
        if 'administrative_area_level_1' in component['types']:
            return component['short_name']
    return None
