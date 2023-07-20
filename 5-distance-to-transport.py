import pandas as pd
from utils.distance_to_coast import get_distance_to_points
import configparser
from utils.constants import SEG_DIST_1, SEG_DIST_2


config = configparser.ConfigParser()
config.read('config.ini')

dft = pd.read_csv('4-transport.csv')
dst = dft.to_xarray()
port = dst.where(dst.type=="port", drop=True)
rail = dst.where(dst.type=="rail", drop=True)


df = pd.read_csv('2-cwns-data-distance.csv')
ds = df.to_xarray()

ds = get_distance_to_points("port", ds, port)
ds = get_distance_to_points("rail", ds, rail)

ds = ds.where((ds.segment_coastline==SEG_DIST_1) | (ds.segment_coastline==SEG_DIST_2), drop=True)

df = ds.to_dataframe()
df = df[['facility_name','cwns_number','state','city','location_description','pres_effluent_treatment_level','disinfection','permit_type','permit','discharge_method','latitude','longitude','population','flow_mgd','flow_lps','dist_to_coastline','dist_to_port','dist_to_rail','segment_coastline','flow_segment','population_segment','segment_port','segment_rail']]
df.to_csv('5-cwns-data-distance-incl-transport.csv')
df.to_excel(f'{config["default"]["project_prefix"]}-cwns-data-distance-incl-transport.xlsx')



df = pd.read_csv('3-power-data-distance.csv')
ds = df.to_xarray()

ds = get_distance_to_points("port", ds, port)
ds = get_distance_to_points("rail", ds, rail)

ds = ds.where( (ds.segment_coastline==SEG_DIST_1) | (ds.segment_coastline==SEG_DIST_2), drop=True)
df = ds.to_dataframe()
df = df[['name','state','city','primary_fuel','water_discharge','latitude','longitude','capacity_mw','generation_gwh_2019', 'flow_mgd','dist_to_coastline','dist_to_port','dist_to_rail','segment_coastline','segment_power','segment_port','segment_rail']]
df.to_csv('5-power-data-distance-incl-transport.csv')
df.to_excel(f'{config["default"]["project_prefix"]}-power-data-distance-incl-transport.xlsx')

