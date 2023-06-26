import pandas as pd
from utils.distance_to_coast import get_distance_to_coast
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

df0 = pd.read_csv('global_power_plant_database.csv')

ds = df0.to_xarray()

dist = get_distance_to_coast(ds, 'United States of America')
dist = dist.drop([ 'country_long', 'gppd_idnr', 'other_fuel1', 'other_fuel2', 'other_fuel3', 'commissioning_year', 'owner', 'source', 'url', 'geolocation_source', 'wepp_id', 'year_of_capacity_data',
                   'generation_gwh_2013', 'generation_gwh_2014', 'generation_gwh_2015', 'generation_gwh_2016', 'generation_gwh_2017', 'generation_gwh_2018', 'generation_gwh_2019', 'generation_data_source', 'estimated_generation_gwh_2013', 'estimated_generation_gwh_2014', 'estimated_generation_gwh_2015', 'estimated_generation_gwh_2016', 'estimated_generation_gwh_2017', 'estimated_generation_note_2013', 'estimated_generation_note_2014', 'estimated_generation_note_2015', 'estimated_generation_note_2016', 'estimated_generation_note_2017'
])

dist2 = dist.where(dist.country=='USA', drop=True)
dist2 = dist2.where(dist.primary_fuel.isin(['Biomass','Coal','Cogeneration','Gas','Nuclear','Oil','Other','Petcoke','Waste']), drop=True)
dist2 = dist2.drop(['country'])
dist2 = dist2.rename({'order_coastline':'order'})

dist2.to_dataframe().to_csv('3-power-data-distance.csv')

filtered = dist2.where(dist2.order<=2, drop=True)
filtered.to_dataframe().to_excel(f'{config["default"]["project_prefix"]}-power-stations.xlsx')