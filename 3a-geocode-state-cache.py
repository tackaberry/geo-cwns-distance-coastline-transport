import pandas as pd
import configparser
from utils.geocode import getStateForLatLon
from utils.constants import SEG_DIST_1, SEG_DIST_2


config = configparser.ConfigParser()
config.read('config.ini')

df = pd.read_csv('3-power-data-distance.csv')

ds = df.to_xarray()

ds = ds.where((ds.segment_coastline==SEG_DIST_1) | (ds.segment_coastline==SEG_DIST_2), drop=True)

ds['facility_state'] = ds.to_dataframe().apply(lambda x: getStateForLatLon(x), axis=1)

ds.to_dataframe().to_csv('3a-geocode-state-cache.csv')

