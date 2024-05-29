import os
import json

import pandas as pd
import geopandas as gpd

from ..utils.os import get_current_path


class Geocoder():
    """
    A class for geocoding geographic coordinates, using either built-in geographic data
    from specified packages or a custom GeoDataFrame provided by the user. It supports
    various geocoding algorithms such as finding nearest regions, regions that contain
    specific coordinates, and regions within a specified distance of coordinates.

    Attributes:
        valid_packages (list): A list of valid package names that can be used to load
                               geographic data from built-in sources.
    
    Methods:
        find_nearest_regions: Finds the nearest geographic regions to the coordinates in the provided DataFrame.
        find_containing_regions: Identifies geographic regions from the provided data sources that contain the coordinates specified in the DataFrame.
        find_regions_within_distance: Finds geographic regions that are within a specified distance from the coordinates in the DataFrame.
        find_all_containing_regions: Identifies all geographic regions from the provided data sources that contain each coordinate in the DataFrame.
        find_all_regions_within_distance: Finds all geographic regions that are within a specified distance from each coordinate in the DataFrame.
    
    Example:
        geocoded_df = Geocoder.find_containing_regions(df, "uk_local_authorities")
    """

    valid_packages = ["countries", "european_countries", "us_states", "us_counties", "uk_local_authorities", "us_primary_roads"]


    def __init__(self, **kwargs):
        """
        Initializes the Geocoder instance with the provided parameters. Dynamically sets
        attributes based on the provided keyword arguments.

        Args:
            df (gpd.GeoDataFrame): A GeoDataFrame containing the geographic coordinates to geocode.
            distance (float, optional): The maximum distance within which to search for regions.
            package_gdf (str, optional): A key representing a geographic data package to load.
            gdf (gpd.GeoDataFrame, optional): A custom GeoDataFrame to use for geocoding.
            Any other keyword arguments will be set as attributes of the instance.

        Raises:
            ValueError: If essential attributes such as 'df' or geographic data references (both 'package_gdf' and 'gdf') are missing.
        """

        # Set attributes from keyword arguments
        for key, value in kwargs.items():
            setattr(self, key, value)
        
        # Ensure the DataFrame and GeoDataFrame are provided
        if not hasattr(self, "df"):
            raise ValueError("Must provide a DataFrame.")
        if not hasattr(self, "package_gdf") and not hasattr(self, "gdf"):
            raise ValueError("Must provide a package_gdf or a custom GeoDataFrame.")
        if self.package_gdf is None and self.gdf is None:
            raise ValueError("Must provide a package_gdf or a custom GeoDataFrame.")

        # Ensure the DataFrame is a GeoDataFrame and has a crs
        if not isinstance(self.df, gpd.GeoDataFrame):
            self.df = gpd.GeoDataFrame(self.df)

        # If no custom GeoDataFrame is provided, load the GeoDataFrame from the package_gdf
        if not hasattr(self, "gdf") or self.gdf is None:
            root_path = os.path.dirname(get_current_path())
            lookup_path = os.path.join(root_path, "data", "geojson", ".lookups.json")

            # Load the GeoDataFrame from the package_gdf
            with open(lookup_path, "r") as file:
                lookups = json.load(file)
                try:
                    geo_file_name = lookups[self.package_gdf]["geo_file"]
                except KeyError:
                    raise ValueError(f"Invalid package_gdf: {self.package_gdf}. Supported options are {list(lookups.keys())}.")
                
                geo_file_path = os.path.join(root_path, "data", "geojson", geo_file_name)
            self.gdf = gpd.read_file(geo_file_path)

            # Remove the id column if present
            if "id" in self.gdf.columns:
                self.gdf.drop(columns=["id"], inplace=True)

        # Ensure latitude and longitude columns are present and rename if necessary
        if "geometry" not in self.df.columns:
            rename_dict = {}
            if "lat" in self.df.columns:
                rename_dict["lat"] = "latitude"
            if "lng" in self.df.columns:
                rename_dict["lng"] = "longitude"
            self.df.rename(columns=rename_dict, inplace=True)
            if "latitude" not in self.df.columns or "longitude" not in self.df.columns:
                raise ValueError("DataFrame must have 'latitude' and 'longitude' columns.")

        # Ensure the DataFrame and GeoDataFrame have the required geometry columns
        if "geometry" not in self.gdf.columns:
            raise ValueError("GeoDataFrame must have a 'geometry' column.")
        if "geometry" not in self.df.columns:
            self.df = self.df.set_geometry(gpd.points_from_xy(self.df["longitude"], self.df["latitude"]))

        # Ensure the DataFrame has a valid CRS
        if self.df.crs is None:
            self.df.crs = self.gdf.crs

        # Ensure the GeoDataFrame is in the same CRS as the DataFrame
        if self.df.crs != self.gdf.crs:
            self.gdf = self.gdf.to_crs(self.df.crs)


    @staticmethod
    def find_nearest_regions(df, package_gdf="countries", gdf=None):
        """
        Finds the nearest geographic regions to the coordinates in the provided DataFrame.

        Args:
            df (gpd.GeoDataFrame): The DataFrame with coordinates to geocode.
            package_gdf (str, optional): The geographic package to use for geocoding.
            gdf (gpd.GeoDataFrame, optional): A custom GeoDataFrame for geocoding.

        Returns:
            gpd.GeoDataFrame: The geocoded DataFrame with additional columns for the geocoded data, minus the geometry column.
        """

        geocoder = Geocoder(df=df, package_gdf=package_gdf, gdf=gdf)
        results = geocoder._find_nearest_regions()

        # Drop the geometry column
        results.drop(columns=["geometry"], inplace=True)
        return results


    @staticmethod
    def find_containing_regions(df, package_gdf="countries", gdf=None):
        """
        Identifies geographic regions from the provided data sources that contain the coordinates specified in the DataFrame.

        Args:
            df (gpd.GeoDataFrame): The DataFrame with coordinates to geocode.
            package_gdf (str, optional): The geographic package to use for geocoding.
            gdf (gpd.GeoDataFrame, optional): A custom GeoDataFrame for geocoding.

        Returns:
            gpd.GeoDataFrame: The geocoded DataFrame with additional columns for the geocoded data, minus the geometry column.
        """

        geocoder = Geocoder(df=df, package_gdf=package_gdf, gdf=gdf)

        # If no polygons or multipolygons are present in the GeoDataFrame, raise an error
        if not any(geocoder.gdf.geom_type.isin(["Polygon", "MultiPolygon"])):
            raise ValueError("GeoDataFrame must contain polygons or multipolygons for region containment geocoding.")

        results = geocoder._find_containing_regions()
        print(results)

        # Drop the geometry column
        results.drop(columns=["geometry"], inplace=True)
        return results


    @staticmethod
    def find_regions_within_distance(df, distance=1000, package_gdf="countries", gdf=None):
        """
        Finds geographic regions that are within a specified distance from the coordinates in the DataFrame.
        If the gdf describe lines or polygons, the distance is calculated as the minimum distance to the boundary.

        Args:
            df (gpd.GeoDataFrame): The DataFrame with coordinates to geocode.
            distance (float): Maximum distance to consider in the unit of the coordinate system of the GeoDataFrame.
            package_gdf (str, optional): The geographic package to use for geocoding.
            gdf (gpd.GeoDataFrame, optional): A custom GeoDataFrame for geocoding.

        Returns:
            gpd.GeoDataFrame: The geocoded DataFrame with additional columns for the geocoded data, minus the geometry column.
        """

        geocoder = Geocoder(df=df, distance=distance, package_gdf=package_gdf, gdf=gdf)
        if geocoder.distance is None:
            raise ValueError("Must provide a maximum distance.")
        
        results = geocoder._find_regions_within_distance()

        # Drop the geometry column
        results.drop(columns=["geometry"], inplace=True)
        return results


    @staticmethod
    def find_all_containing_regions(df, package_gdf="countries", gdf=None):
        """
        NOT YET IMPLEMENTED
        Identifies all geographic regions from the provided data sources that contain each coordinate in the DataFrame.
        Returns multiple rows for each coordinate if multiple regions contain the coordinate.

        Args:
            df (gpd.GeoDataFrame): The DataFrame with coordinates to geocode.
            package_gdf (str, optional): The geographic package to use for geocoding.
            gdf (gpd.GeoDataFrame, optional): A custom GeoDataFrame for geocoding.

        Returns:
            gpd.GeoDataFrame: The geocoded DataFrame with additional columns for the geocoded data, including all matching regions, minus the geometry column.
        """

        geocoder = Geocoder(df=df, package_gdf=package_gdf, gdf=gdf)

        # If no polygons or multipolygons are present in the GeoDataFrame, raise an error
        if not any(geocoder.gdf.geom_type.isin(["Polygon", "MultiPolygon"])):
            raise ValueError("GeoDataFrame must contain polygons or multipolygons for region containment geocoding.")

        results = geocoder._find_all_containing_regions()

        # Drop the geometry column
        results.drop(columns=["geometry"], inplace=True)
        return results
    

    @staticmethod
    def find_all_regions_within_distance(df, distance=1000, package_gdf="countries", gdf=None):
        """
        NOT YET IMPLEMENTED
        Finds all geographic regions that are within a specified distance from each coordinate in the DataFrame.
        Returns multiple rows for each coordinate if multiple regions are within the specified distance.

        Args:
            df (gpd.GeoDataFrame): The DataFrame with coordinates to geocode.
            distance (float): Maximum distance to consider in the unit of the coordinate system of the GeoDataFrame.
            package_gdf (str, optional): The geographic package to use for geocoding.
            gdf (gpd.GeoDataFrame, optional): A custom GeoDataFrame for geocoding.

        Returns:
            gpd.GeoDataFrame: The geocoded DataFrame with additional columns for the geocoded data, including all matching regions within the specified distance, minus the geometry column.
        """

        geocoder = Geocoder(df=df, distance=distance, package_gdf=package_gdf, gdf=gdf)
        if geocoder.distance is None:
            raise ValueError("Must provide a maximum distance.")
        
        results = geocoder._find_all_regions_within_distance()

        # Drop the geometry column
        results.drop(columns=["geometry"], inplace=True)
        return results
    

    def _find_nearest_regions(self):
        """
            Helper method to interact with the Geocoder instance to perform the geocoding operation.
        """

        # Convert data to an appropriate CRS for distance calculation
        original_crs = self.df.crs
        utm_crs = self.df.estimate_utm_crs() 
        self.df = self.df.to_crs(utm_crs)
        self.gdf = self.gdf.to_crs(utm_crs)

        # First, check which points are within regions
        within_df = self._find_containing_regions()
        contained_df = within_df[within_df["geocoded"] == "within_region"].copy()
        not_contained_df = within_df[within_df["geocoded"] == "outside_boundary"].copy()
        contained_df["distance"] = 0  # Points inside regions have zero distance

        # Drop new columns from not_contained_df
        new_columns = [col for col in not_contained_df.columns if col not in self.df.columns]
        not_contained_df.drop(columns=new_columns, inplace=True)

        # Handle cases where some points are not contained within any region
        if not not_contained_df.empty:

            # Calculate distances to the nearest region boundary for points not contained within any region
            nearest_df = gpd.sjoin_nearest(not_contained_df, self.gdf, how="left", distance_col="distance")
            nearest_df["geocoded"] = "nearest_region"

            # Clean up columns from the join
            if "index_right" in nearest_df.columns:
                nearest_df.drop(columns=["index_right"], inplace=True)

            # Combine the results from the two sets of points
            result_df = pd.concat([contained_df, nearest_df], ignore_index=True)
        
        # Handle case where all points are contained within regions
        else:
            within_df["distance"] = 0
            result_df = within_df

        # Convert back to original CRS
        result_df = result_df.to_crs(original_crs)

        return result_df


    def _find_containing_regions(self):
        """
            Helper method to interact with the Geocoder instance to perform the geocoding operation.
        """

        # Perform spatial join to find points within regions
        result_df = gpd.sjoin(self.df, self.gdf, how="left", predicate="within")
        result_df["geocoded"] = result_df["index_right"].notnull().replace({True: "within_region", False: "outside_boundary"})
        result_df.drop(columns=["index_right"], inplace=True)

        # Drop the id_right column from the GeoDataFrame
        if "id_right" in result_df.columns:
            result_df.drop(columns=["id_right"], inplace=True)

        return result_df


    def _find_regions_within_distance(self):
        """
            Helper method to interact with the Geocoder instance to perform the geocoding operation.
        """
    
        # Convert data to an appropriate CRS for distance calculation
        original_crs = self.df.crs
        utm_crs = self.df.estimate_utm_crs()
        self.df = self.df.to_crs(utm_crs)
        self.gdf = self.gdf.to_crs(utm_crs)

        # Check which points are within the regions
        within_df = self._find_containing_regions()
        contained_df = within_df[within_df["geocoded"] == "within_region"].copy()
        not_contained_df = within_df[within_df["geocoded"] == "outside_boundary"].copy()
        contained_df["distance"] = 0  # Points inside regions have zero distance

        # Drop new columns from not_contained_df
        new_columns = [col for col in not_contained_df.columns if col not in self.df.columns]
        not_contained_df.drop(columns=new_columns, inplace=True)

        # Handle case where some points are not contained within any region
        if not not_contained_df.empty:

            # Calculate distances to the nearest region boundary
            nearest_df = gpd.sjoin_nearest(not_contained_df, self.gdf, how="left", distance_col="distance")
            nearest_df["geocoded"] = nearest_df["distance"].apply(lambda x: "within_distance" if x <= self.distance else "outside_boundary")
            
            # Clean up columns from the join]
            if "index_right" in nearest_df.columns:
                nearest_df.drop(columns=["index_right"], inplace=True)

            # Combine the results from the two sets of points
            result_df = pd.concat([contained_df, nearest_df], ignore_index=True)
        
        # Handle case where all points are contained within regions
        else:
            within_df["distance"] = 0
            result_df = within_df

        # Convert back to original CRS
        result_df = result_df.to_crs(original_crs)

        return result_df


    def _find_all_containing_regions(self):
        """
            Helper method to interact with the Geocoder instance to perform the geocoding operation.
        """


    def _find_all_regions_within_distance(self):
        """
            Helper method to interact with the Geocoder instance to perform the geocoding operation.
        """
