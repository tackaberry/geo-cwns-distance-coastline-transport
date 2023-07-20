import pandas as pd
import numpy as np
import configparser
from utils.geocode import getStateForLatLon
from utils.constants import SEG_DIST_1, SEG_DIST_2


config = configparser.ConfigParser()
config.read('config.ini')

df = pd.read_csv('3-power-data-distance.csv')
ds = df.to_xarray()

dfw = pd.read_excel('cooling_summary_2019.xlsx', sheet_name='Summary', header=2)
dsw = dfw.to_xarray()

def getWater(x):
    print(x.gppd_idnr)
    code = int(x.gppd_idnr[3:])
    plant = dsw.where(dsw["Plant Code"]==code, drop=True)
    water = pd.to_numeric(plant["Water Withdrawal Volume (Million Gallons)"], errors='coerce')
    water = water[~np.isnan(water)]
    sum = (water.sum())/365
    water_discharge = None
    if plant["Water Discharge Name"].size and not plant["Water Discharge Name"].values[0] == 'nan': 
            water_discharge = plant["Water Discharge Name"].values[0]
    return [sum, water_discharge ]

water_discharge = ds.to_dataframe().apply(lambda x: getWater(x), axis=1)
ds["flow_mgd"] = water_discharge.apply(lambda x: x[0])
ds["water_discharge"] = water_discharge.apply(lambda x: x[1])

ds.to_dataframe().to_csv('3-power-data-distance.csv')
