import requests
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['default']['google_search_api_key']

term = '"MS0034436" npdes permit type:pdf'

x = requests.get(f'https://www.googleapis.com/customsearch/v1?key={api_key}&cx=4078f5ea249074bf8&q={term}')
