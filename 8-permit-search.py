import requests
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['default']['google_search_api_key']
search_cx = config['default']['google_search_cx']


term = '"MS0034436" npdes permit type:pdf'

x = requests.get(f'https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_cx}&q={term}')
