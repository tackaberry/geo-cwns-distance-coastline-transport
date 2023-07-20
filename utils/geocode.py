import googlemaps
import numpy as np
import configparser

config = configparser.ConfigParser()
config.read('config.ini')


gmaps = googlemaps.Client(key=config['default']['google_api_key'])

def getStateForLatLon(x):
    city = None
    state = None
    result = gmaps.reverse_geocode((x.latitude, x.longitude))
    for component in result[0]['address_components']:
        if 'locality' in component['types']:
            city = component['long_name']
        if 'administrative_area_level_1' in component['types']:
            state = component['short_name']
    return [city, state]
