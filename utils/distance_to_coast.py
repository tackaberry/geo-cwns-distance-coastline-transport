import geopandas as gpd
import cartopy
import numpy as np
import xarray as xr
import pandas as pd
import shapely

def hv(name, lonlat1, lonlat2):
    AVG_EARTH_RADIUS = 6371000. # Earth radius in meter

    # Get array data; convert to radians to simulate 'map(radians,...)' part
    coords_arr = np.deg2rad(lonlat1)
    a = np.deg2rad(lonlat2)

    # Get the differentiations
    lat = coords_arr[:,1] - a[:,1,None]
    lng = coords_arr[:,0] - a[:,0,None]

    # Compute the "cos(lat1) * cos(lat2) * sin(lng * 0.5) ** 2" part.
    # Add into "sin(lat * 0.5) ** 2" part.
    add0 = np.cos(a[:,1,None])*np.cos(coords_arr[:,1])* np.sin(lng * 0.5) ** 2
    d = np.sin(lat * 0.5) ** 2 +  add0

    # Get h and assign into dataframe
    h = 2 * AVG_EARTH_RADIUS * np.arcsin(np.sqrt(d))
    d1 = h.min(1)/1000

    order_list = [d1<5, d1<10, d1<100, d1<1000, d1>=1000]
    choice_list = [1, 2, 3, 4, 5]
    order = np.select(order_list, choice_list, default=0)

    obj = {}
    obj[f'dist_to_{name}'] = d1
    obj[f'order_{name}'] = order

    return obj

def get_distance_to_coast(arr, country, resolution='50m'):

    print('Get shape file...')
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    #single geom for country
    geom = world[world["name"]==country].dissolve(by='name').iloc[0].geometry

    #single geom for the coastline
    c = cartopy.io.shapereader.natural_earth(resolution=resolution, category='physical', name='coastline')

    c     = gpd.read_file(c)
    c.crs = 'EPSG:4326'

    points = []
    dfp = arr.to_dataframe()
    for i in range(len(dfp)):
        points.append([dfp.iloc[i].longitude, dfp.iloc[i].latitude])

    xlist = []
    gdpclip = gpd.clip(c.to_crs('EPSG:4326'), geom.buffer(1))
    for icoast in range(len(gdpclip)):
        print('Get coastline ({}/{})...'.format(icoast+1, len(gdpclip)))
        coastline = gdpclip.iloc[icoast].geometry #< This is a linestring

        if type(coastline) is shapely.geometry.linestring.LineString:
            coastline = [list(i) for i in coastline.coords]
        elif type(coastline) is shapely.geometry.multilinestring.MultiLineString:
            dummy = []
            for line in list(coastline.geoms):
                dummy.extend([list(i) for i in line.coords])
            coastline = dummy
        else:
            print('In function: get_distance_to_coast')
            print('Type: {} not found'.format(type(type(coastline))))
            exit()

        print('Computing distances...')
        result = hv("coastline", coastline, points)

        print('Convert to xarray...')
        gdf = gpd.GeoDataFrame.from_records(result)
        df1 = pd.DataFrame(gdf)
        xlist.append(df1.to_xarray())
    
    xarr = xr.concat(xlist, dim='icoast').min('icoast')

    return xr.merge([arr, xarr])
 
def get_distance_to_points(name, arr1, arr2):
    
    points1 = []
    df1 = arr1.to_dataframe()
    for i in range(len(df1)):
        points1.append([df1.iloc[i].longitude, df1.iloc[i].latitude])

    points2 = []
    df2 = arr2.to_dataframe()
    for i in range(len(df2)):
        points2.append([df2.iloc[i].longitude, df2.iloc[i].latitude])

    result = hv(name, points2, points1)
    result["index"] = df1.index.values
    
    gdf = gpd.GeoDataFrame.from_records(result)
    df3 = pd.DataFrame(gdf)
    
    xarr = df3.to_xarray()

    return xr.merge([arr1, xarr], )