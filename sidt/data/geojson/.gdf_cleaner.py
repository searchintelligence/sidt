import os
import json

import pandas as pd
import geopandas as gpd

from sidt.utils.os import get_current_path
from sidt.utils.io import CLIF


def load_geojson(geojson_file):
    """Load a GeoJSON file into a GeoDataFrame."""

    file_path = os.path.join(get_current_path(), geojson_file)

    gdf = gpd.read_file(file_path)

    if "id" in gdf.columns:
        gdf.drop(columns=["id"], inplace=True)

    return gdf


def load_shp(shp_folder):
    """Load a folder containing shp into a GeoDataFrame."""

    folder_path = os.path.join(get_current_path(), shp_folder)
    shp_file_name = [file for file in os.listdir(folder_path) if file.endswith('.shp')][0]
    file_path = os.path.join(folder_path, shp_file_name)
    gdf = gpd.read_file(file_path)
    return gdf


def save_geojson(gdf, geojson_file, minify=True):
    """Save a GeoDataFrame to a GeoJSON file. Supports minification."""

    file_path = os.path.join(get_current_path(), geojson_file)

    if minify:
        geojson_str = gdf.to_json()
        minified_geojson = json.dumps(json.loads(geojson_str), separators=(",", ":"))
        with open(file_path, "w") as file:
            file.write(minified_geojson)
    else:
        gdf.to_file(file_path, driver="GeoJSON")


def save_to_csv(gdf, file_name, drop_geometry=True):
    """Save a GeoDataFrame to a CSV file."""

    file_path = os.path.join(get_current_path(), file_name)

    if drop_geometry and "geometry" in gdf.columns:
        gdf = gdf.drop(columns="geometry")
    gdf.to_csv(file_path, index=False)


def inspect_gdf(gdf, head=True, col_names=True, geometry=True, crs=True):
    """Inspect the GeoDataFrame by printing its head, column names, geometry, and CRS."""

    if head:
        print(CLIF.fmt("Head of GeoDataFrame:\n", CLIF.Color.RED), gdf.head())
    if col_names:
        print(CLIF.fmt("Column Names:\n", CLIF.Color.RED), gdf.columns)
    if geometry:
        print(CLIF.fmt("Geometry:\n", CLIF.Color.RED), gdf.geometry)
    if crs:
        print(CLIF.fmt("CRS:\n", CLIF.Color.RED), gdf.crs)


def simplify_geometry(gdf, tolerance=0.001):
    """Simplify the geometry of a GeoDataFrame."""
    gdf["geometry"] = gdf["geometry"].simplify(tolerance=tolerance, preserve_topology=True)
    return gdf


def convert_to_wgs84(gdf):
    """Convert the geometry of a GeoDataFrame to WGS84."""
    if gdf.crs.to_epsg() != 4326:
        gdf = gdf.to_crs(epsg=4326)
    return gdf


if __name__ == "__main__":
    # gdf = load_shp("us_primary_roads")
    # inspect_gdf(gdf)
    # gdf = gdf.drop(columns=["MTFCC"])
    # gdf = gdf.rename(columns={
    #     "LINEARID": "tiger_line_road_segment_linear_id",
    #     "FULLNAME": "road_name",
    #     "RTTYP": "road_type",
    # })
    # inspect_gdf(gdf)


    # save_geojson(gdf, "us_primary_roads.geojson")

    # gdf = load_geojson("us_primary_roads.geojson")
    # inspect_gdf(gdf)

    for file in os.listdir(get_current_path()):
        if file.endswith(".geojson"):
            gdf = load_geojson(file)
            inspect_gdf(gdf)
            input("Press Enter to continue...")