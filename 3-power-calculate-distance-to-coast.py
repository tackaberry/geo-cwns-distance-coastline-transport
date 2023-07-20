import pandas as pd
from utils.distance_to_coast import get_distance_to_coast
import configparser
from utils.constants import SEG_DIST_1, SEG_DIST_2, seg_power

config = configparser.ConfigParser()
config.read('config.ini')

df0 = pd.read_csv('global_power_plant_database.csv')

df_cache = pd.read_csv('3a-geocode-state-cache.csv')
ds_cache = df_cache.to_xarray()


ds = df0.to_xarray()

dist = get_distance_to_coast(ds, config['default']['coastlines_country'])

dist = dist.drop([ 'country_long',  'other_fuel1', 'other_fuel2', 'other_fuel3', 'commissioning_year', 'owner', 'source', 'url', 'geolocation_source', 'wepp_id', 'year_of_capacity_data',
                   'generation_gwh_2013', 'generation_gwh_2014', 'generation_gwh_2015', 'generation_gwh_2016', 'generation_gwh_2017', 'generation_gwh_2018', 'generation_data_source', 'estimated_generation_gwh_2013', 'estimated_generation_gwh_2014', 'estimated_generation_gwh_2015', 'estimated_generation_gwh_2016', 'estimated_generation_gwh_2017', 'estimated_generation_note_2013', 'estimated_generation_note_2014', 'estimated_generation_note_2015', 'estimated_generation_note_2016', 'estimated_generation_note_2017'
])

dist = dist.where(dist.country==config['default']['powerplant_country'], drop=True)
dist = dist.where(dist.primary_fuel.isin(['Biomass','Coal','Cogeneration','Gas','Oil','Other','Petcoke','Waste']), drop=True)
dist = dist.drop(['country'])

dist = dist.where((dist.segment_coastline==SEG_DIST_1) | (dist.segment_coastline==SEG_DIST_2), drop=True)


dist['segment_power'] = dist.to_dataframe().apply(lambda x: seg_power(x), axis=1)

def get_state(x):
    found = ds_cache.where( (ds_cache['latitude']==x.latitude) & (ds_cache['longitude']==x.longitude), drop=True).to_dataframe()
    if not found.empty:
        return found['state'].values[0]
    else:
        return 'unknown'

def get_city(x):
    found = ds_cache.where( (ds_cache['latitude']==x.latitude) & (ds_cache['longitude']==x.longitude), drop=True).to_dataframe()
    if not found.empty:
        return found['city'].values[0]
    else:
        return 'unknown'

dist['state'] = dist.to_dataframe().apply(lambda x: get_state(x), axis=1)
dist['city'] = dist.to_dataframe().apply(lambda x: get_city(x), axis=1)


dist.to_dataframe().to_csv('3-power-data-distance.csv')
dist.to_dataframe().to_excel(f'{config["default"]["project_prefix"]}-power-stations.xlsx')