import pandas as pd
from utils.distance_to_coast import get_distance_to_coast
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

df0 = pd.read_csv('1-cwns.csv')

ds = df0.to_xarray()

ds['flow_lps'] = ds.flow_mgd * 3785411.8 / 86400

dist = get_distance_to_coast(ds, 'United States of America')
dist = dist.rename({'order_coastline':'order'})

dist.to_dataframe().to_csv('2-cwns-data-distance.csv')

filtered = dist.where(dist.order<=2, drop=True)
filtered.to_dataframe().to_excel(f'{config["default"]["project_prefix"]}-cwns.xlsx')