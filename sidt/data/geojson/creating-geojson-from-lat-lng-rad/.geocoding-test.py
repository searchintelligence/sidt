import os
import json

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

from sidt.utils.os import get_current_path
from sidt.utils.io import CLIF
from sidt.utils.geocoders import Geocoder, GeoPackages




data_points = [
    {
        "point": "no_overlap",
        "lng": -97.33,
        "lat": 32.765,
    },
    {
        "point": "overlap",
        "lng": -97.186,
        "lat": 32.726,
    },
    {
        "point": "not_in_zone",
        "lng": -97.181,
        "lat": 33.029
    }
]

df = pd.DataFrame(data_points)

gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lng, df.lat), crs="EPSG:4326")

countries = GeoPackages().load_gdf("countries")

print(countries)
print(countries.columns)






geocoded = Geocoder(df, "countries", distance=100).geocode()

print(geocoded)






