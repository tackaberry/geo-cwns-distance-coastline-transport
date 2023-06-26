import pandas as pd
from utils.distance_to_coast import get_distance_to_coast
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

dfp = pd.read_csv('Intermodal_Freight_Facilities_Marine_Roll-on_Roll-off.csv')
dfp1 = dfp[['OBJECTID','PORT', 'LAT', 'LON']]
dfp2 = dfp1.rename(columns={'PORT':'name', 'OBJECTID':'object_id','LAT':'latitude','LON':'longitude'})
dfp2['type'] = ['port']*len(dfp2) 
dfp2["object_id"] = dfp2["object_id"] + 10000

dfr = pd.read_csv('Intermodal_Freight_Facilities_Rail_TOFC_COFC.csv')
dfr1 = dfr[['OBJECTID','TERMINAL', 'LAT', 'LON']]
dfr2 = dfr1.rename(columns={'TERMINAL':'name', 'OBJECTID':'object_id','LAT':'latitude','LON':'longitude'})
dfr2['type'] = ['rail']*len(dfr2)
dfr2["object_id"] = dfr2["object_id"] + 20000

df = pd.concat([dfp2, dfr2],  axis=0, ignore_index=True)
ds = df.to_xarray()
dist = get_distance_to_coast(ds, 'United States of America')
dist = dist.rename({'order_coastline':'order'})

filtered = dist.where(dist.order<=3, drop=True)

filtered.to_dataframe().to_csv('4-transport.csv')
