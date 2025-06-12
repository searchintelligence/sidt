import os
import json

import pandas as pd
import geopandas as gpd


class Geocoder:

    def __init__(self, points, package_gdf=None, gdf=None, distance=None):

        # Buffer distance
        self.distance = distance if distance is not None else 0
        
        if points is None:
            raise ValueError("Must provide a DataFrame.")

        packages = GeoPackages()
        valid_packages = packages.list_packages()

        if gdf is None:
            if package_gdf is None:
                raise ValueError("Must provide either package_gdf or gdf.")
            if package_gdf not in valid_packages:
                raise ValueError(f"Invalid package_gdf: {package_gdf}. Supported options are {valid_packages}.")
            gdf = packages.load_gdf(package_gdf)

        # If not already a GeoDataFrame, make it one
        if not isinstance(points, gpd.GeoDataFrame):
            points = gpd.GeoDataFrame(points)

        # Only construct geometry if missing
        if "geometry" not in points.columns:

            # Find case-insensitive latitude and longitude columns
            col_map = {col.lower(): col for col in points.columns}
            lat_names = {"lat", "latitude"}
            lng_names = {"lng", "longitude", "long", "lon"}
            lat_col = next((col_map[name] for name in lat_names if name in col_map), None)
            lng_col = next((col_map[name] for name in lng_names if name in col_map), None)

            if lat_col is None or lng_col is None:
                raise ValueError(
                    "DataFrame must include a 'geometry' column or a valid latitude and longitude column "
                    "(case-insensitive, any of: lat/latitude and lng/longitude/long/lon)."
                )
            points = gpd.GeoDataFrame(
                points,
                geometry=gpd.points_from_xy(points[lng_col], points[lat_col]),
                crs="EPSG:4326"
            )

        # Ensure the CRS is set
        if points.crs is None:
            points.crs = "EPSG:4326"
        if gdf.crs is None:
            gdf.crs = "EPSG:4326"
        
        # Prefix all gdf columns with 'gdf_' to avoid conflicts with df columns, except for the geometry column
        gdf.columns = [f"gc_gdf_{col}" if col != "geometry" else col for col in gdf.columns]

        self.df = points
        self.gdf = gdf
    

    def geocode(self):
        
        # Convert to projected CRS for distance calculation
        original_crs = self.df.crs
        utm_crs = self.df.estimate_utm_crs()

        self.df = self.df.to_crs(utm_crs)
        self.gdf = self.gdf.to_crs(utm_crs)

        buffered_gdf = self.gdf.copy()
        buffered_gdf["geometry"] = buffered_gdf.geometry.buffer(0)
        buffered_gdf["geometry"] = buffered_gdf.geometry.buffer(self.distance)


        # Spatial join: points within buffered regions
        joined = gpd.sjoin(self.df, buffered_gdf, how="left", predicate="within")

        # Mark everything matched as within_region, others as outside_boundary
        joined["gc_is_geocoded"] = joined["index_right"].notnull().map({True: "within_region", False: "outside_boundary"})

        if "index_right" in joined.columns:
            joined.drop(columns=["index_right"], inplace=True)

        # Convert back to original CRS
        result_df = joined.to_crs(original_crs)

        return result_df


class GeoPackages():
    """
    A class for browsing, managing, and accessing GeoJSON files within the geojson directory.

    Attributes:
        root_path (str): The root directory of the GeoJSON data files.
        lookup_path (str): The path to the lookup file containing metadata about available GeoJSON files.
        available_packages (list): A list of all available packages based on the lookup file.
    """

    from sidt.utils.os import get_current_path

    def __init__(self):
        """
        Initializes the GeoJSON class by setting up paths and loading metadata from the lookup file.
        """

        self.root_path = os.path.dirname(GeoPackages.get_current_path())
        self.geojson_dir = os.path.join(self.root_path, "data", "geojson")
        self.lookup_path = os.path.join(self.geojson_dir, ".lookups.json")

        if not os.path.exists(self.lookup_path):
            raise FileNotFoundError(f"Lookup file not found: {self.lookup_path}")

        with open(self.lookup_path, "r") as file:
            self.lookups = json.load(file)

        self.available_packages = list(self.lookups.keys())


    def list_packages(self):
        """
        Lists all available GeoJSON packages.

        Returns:
            list: A list of available GeoJSON package names.
        """
        return self.available_packages


    def get_geojson_file_path(self, package_name):
        """
        Retrieves the file path of the GeoJSON file for a given package.

        Args:
            package_name (str): The name of the package.

        Returns:
            str: The file path of the GeoJSON file.

        Raises:
            ValueError: If the package_name is not valid.
        """
        if package_name not in self.lookups:
            raise ValueError(f"Invalid package name: {package_name}. Available packages: {self.available_packages}")

        return os.path.join(self.geojson_dir, self.lookups[package_name]["geo_file"])


    def load_gdf(self, package_name):
        """
        Loads a GeoDataFrame from the specified package.

        Args:
            package_name (str): The name of the package.

        Returns:
            gpd.GeoDataFrame: The loaded GeoDataFrame.
        """
        file_path = self.get_geojson_file_path(package_name)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"GeoJSON file not found: {file_path}")

        return gpd.read_file(file_path)


    def get_columns(self, package_name):
        """
        Retrieves the column names of the GeoDataFrame for a specified GeoJSON package.

        Args:
            package_name (str): The name of the package.

        Returns:
            list: A list of column names in the GeoDataFrame.
        """
        gdf = self.load_gdf(package_name)
        return gdf.columns.tolist()


    def get_geometry(self, package_name, key=None, key_column="name", as_list=False):
        """
        Retrieves the geometries from a GeoJSON package.

        Args:
            package_name (str): The name of the package.
            key (str, optional): The value to match in the specified key_column. Defaults to None.
            key_column (str, optional): The column to match the key against. Defaults to "name".
            as_list (bool, optional): If True, returns a list of geometry objects. Defaults to False.

        Returns:
            shapely.geometry or list: The geometry object(s) from the package or a specific geometry matching the key.
        """
        gdf = self.load_gdf(package_name)
        
        # If a specific key is provided, filter the GeoDataFrame
        if key:
            if key_column not in gdf.columns:
                raise ValueError(f"Column '{key_column}' not found in GeoDataFrame.")
            
            # Filter the GeoDataFrame for the specific key
            filtered_gdf = gdf[gdf[key_column] == key]
            if filtered_gdf.empty:
                raise ValueError(f"No geometry found for key '{key}' in column '{key_column}'.")

            if as_list:
                return filtered_gdf["geometry"].tolist()
            return filtered_gdf["geometry"].iloc[0]  # Return the first match

        # Return all geometries if no key is specified
        if as_list:
            return gdf["geometry"].tolist()
        return gdf["geometry"]


    def get_bounds(self, package_name):
        """
        Retrieves the bounding box of the geometries in a GeoJSON package.

        Args:
            package_name (str): The name of the package.

        Returns:
            tuple: A tuple representing the bounding box (minx, miny, maxx, maxy).
        """
        gdf = self.load_gdf(package_name)
        return gdf.total_bounds


    def get_crs(self, package_name):
        """
        Retrieves the coordinate reference system (CRS) of a GeoJSON package.

        Args:
            package_name (str): The name of the package.

        Returns:
            dict or str: The CRS of the package.
        """
        gdf = self.load_gdf(package_name)
        return gdf.crs

