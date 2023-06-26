import pandas as pd
from utils.distance_to_coast import get_distance_to_points
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

dft = pd.read_csv('4-transport.csv')
dst = dft.to_xarray()
port = dst.where(dst.type=="port", drop=True)
rail = dst.where(dst.type=="rail", drop=True)


df = pd.read_csv('2-cwns-data-distance.csv')
ds = df.to_xarray()

dist = get_distance_to_points("port", ds, port)
dist = get_distance_to_points("rail", dist, rail)

dist = dist.where(dist.order<=2, drop=True)

dist.to_dataframe().to_csv('5-cwns-data-distance-incl-transport.csv')
dist.to_dataframe().to_excel(f'{config["default"]["project_prefix"]}-cwns-data-distance-incl-transport.xlsx')



df = pd.read_csv('3-power-data-distance.csv')
ds = df.to_xarray()

dist = get_distance_to_points("port", ds, port)
dist = get_distance_to_points("rail", dist, rail)

dist = dist.where(dist.order<=2, drop=True)

dist.to_dataframe().to_csv('5-power-data-distance-incl-transport.csv')
dist.to_dataframe().to_excel(f'{config["default"]["project_prefix"]}-power-data-distance-incl-transport.xlsx')

