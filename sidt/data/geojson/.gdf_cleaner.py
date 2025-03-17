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

    gdf = load_geojson("canada_provinces.geojson")
    inspect_gdf(gdf)
    
    # remove columns except geometry, prov_name_en, prov_code
    gdf = gdf.drop(columns=[col for col in gdf.columns if col not in ["geometry", "prov_name_en", "prov_code"]])

    # convert prov_code and prov_name_en to strings by extracting the first element in the list values in the columns
    gdf["prov_code"] = gdf["prov_code"].apply(lambda x: x[0] if isinstance(x, list) else x)
    gdf["prov_name_en"] = gdf["prov_name_en"].apply(lambda x: x[0] if isinstance(x, list) else x)

    # rename columns to prov_code and prov_name_en
    gdf = gdf.rename(columns={"prov_code": "code", "prov_name_en": "name"})

    # save the cleaned GeoDataFrame
    inspect_gdf(gdf)
    save_geojson(gdf, "canada_provinces.geojson")