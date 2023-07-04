import pandas as pd
import xarray as xr
from utils.distance_to_coast import get_distance_to_coast
import configparser
from utils.constants import SEG_DIST_1, SEG_DIST_2, MGD_TO_LPS, seg_flow, seg_pop


config = configparser.ConfigParser()
config.read('config.ini')

df0 = pd.read_csv('1-cwns.csv')

ds = df0.to_xarray()

ds['flow_lps'] = ds.flow_mgd * MGD_TO_LPS

ds['flow_segment'] = ds.to_dataframe().apply(lambda x: seg_flow(x), axis=1)
ds['population_segment'] = ds.to_dataframe().apply(lambda x: seg_pop(x), axis=1)

dist = get_distance_to_coast(ds, config['default']['coastlines_country'])
dist = dist.where( (dist.segment_coastline==SEG_DIST_1) | (dist.segment_coastline==SEG_DIST_2), drop=True)

dist.to_dataframe().to_csv('2-cwns-data-distance.csv')

dist.to_dataframe().to_excel(f'{config["default"]["project_prefix"]}-cwns.xlsx')