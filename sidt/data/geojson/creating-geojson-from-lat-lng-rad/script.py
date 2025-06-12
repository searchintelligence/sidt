import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import sys
import os

# Setup directory path
dir = sys.path[0]

# Read Excel files
df_cities = pd.read_excel(os.path.join(dir, "us_cities.xlsx"), index_col=None)

# Convert df_cities and df_hotels to GeoDataFrames with WGS84 CRS
gdf_cities = gpd.GeoDataFrame(df_cities, geometry=gpd.points_from_xy(df_cities["lng"], df_cities["lat"]))
gdf_cities.crs = "EPSG:4326"

# Convert to a common CRS that measures distance in meters (EPSG:3857)
gdf_cities = gdf_cities.to_crs(epsg=3857)

# Buffer each city by its radius (converted to meters) and create a new GeoDataFrame for the buffered cities
gdf_cities["buffer"] = gdf_cities.geometry.buffer(gdf_cities["radius"] * 1000)
gdf_cities_buffer = gpd.GeoDataFrame(gdf_cities, geometry="buffer")
gdf_cities_buffer.crs = "EPSG:3857"

gdf_cities_buffer = gdf_cities_buffer[["buffer", "city", "state", "lat", "lng", "radius", "si-regional-data-lookup"]]


gdf_cities_buffer = gdf_cities_buffer.to_crs(epsg=4326)


gdf_cities_buffer.to_file(os.path.join(dir, "cities_buffer.geojson"), driver="GeoJSON")
