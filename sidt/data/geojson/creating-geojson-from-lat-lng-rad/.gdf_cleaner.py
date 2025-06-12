import os
import json

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

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


def plot_gdf(gdf, title="GeoDataFrame Plot", figsize=(10, 10), color="lightblue", edgecolor="black"):
    fig, ax = plt.subplots(figsize=figsize)
    gdf.plot(ax=ax, color=color, edgecolor=edgecolor)
    ax.set_title(title)
    plt.axis("equal")
    plt.show()


if __name__ == "__main__":

    gdf = load_geojson("countries_raw.geojson")

    # filter out the countries listed
    non_countries = [
        "Dhekelia Sovereign Base Area", "Saint Martin", "Sint Maarten", "US Naval Base Guantanamo Bay", "Brazilian Island",
        "Cyprus No Mans Area", "Siachen Glacier", "Baykonur Cosmodrome", "Akrotiri Sovereign Base Area",
        "Southern Patagonian Ice Field", "Bir Tawil", "Antarctica", "New Caledonia", "CuraÃ§ao", "Aruba",
        "Ashmore and Cartier Islands", "Bajo Nuevo Bank (Petrel Is.)", "Serranilla Bank", "Scarborough Reef",
        "Coral Sea Islands", "Spratly Islands", "Clipperton Island", "American Samoa", "Guam",
        "Turks and Caicos Islands", "Saint Pierre and Miquelon", "Pitcairn Islands", "French Polynesia",
        "French Southern and Antarctic Lands", "United States Minor Outlying Islands", "Montserrat",
        "United States Virgin Islands", "Saint Barthelemy", "Puerto Rico", "British Virgin Islands",
        "Cayman Islands", "Heard Island and McDonald Islands", "Jersey", "Guernsey", "Isle of Man", "Aland",
        "Faroe Islands", "Indian Ocean Territories", "British Indian Ocean Territory", "Norfolk Island",
        "Cook Islands", "Wallis and Futuna", "South Georgia and the Islands", "Falkland Islands", "Niue",
        "Gibraltar", "Northern Mariana Islands", "Curaçao", "Anguilla", "Bermuda", "Saint Helena", "Vatican"
    ]

    gdf = gdf[~gdf["name"].isin(non_countries)]

    #add region column
    country_to_region = {
        "Indonesia": "South-Eastern Asia",
        "Malaysia": "South-Eastern Asia",
        "Chile": "South America",
        "Bolivia": "South America",
        "Peru": "South America",
        "Argentina": "South America",
        "Cyprus": "Western Asia",
        "India": "Southern Asia",
        "China": "Eastern Asia",
        "Israel": "Western Asia",
        "Palestine": "Western Asia",
        "Lebanon": "Western Asia",
        "Ethiopia": "Eastern Africa",
        "South Sudan": "Eastern Africa",
        "Somalia": "Eastern Africa",
        "Kenya": "Eastern Africa",
        "Malawi": "Eastern Africa",
        "United Republic of Tanzania": "Eastern Africa",
        "Syria": "Western Asia",
        "Somaliland": "Eastern Africa",
        "France": "Western Europe",
        "Suriname": "South America",
        "Guyana": "South America",
        "South Korea": "Eastern Asia",
        "North Korea": "Eastern Asia",
        "Morocco": "Northern Africa",
        "Western Sahara": "Northern Africa",
        "Costa Rica": "Central America",
        "Nicaragua": "Central America",
        "Republic of the Congo": "Middle Africa",
        "Democratic Republic of the Congo": "Middle Africa",
        "Bhutan": "Southern Asia",
        "Ukraine": "Eastern Europe",
        "Belarus": "Eastern Europe",
        "Namibia": "Southern Africa",
        "South Africa": "Southern Africa",
        "Oman": "Western Asia",
        "Uzbekistan": "Central Asia",
        "Kazakhstan": "Central Asia",
        "Tajikistan": "Central Asia",
        "Lithuania": "Northern Europe",
        "Brazil": "South America",
        "Uruguay": "South America",
        "Mongolia": "Eastern Asia",
        "Russia": "Northern Asia",
        "Czechia": "Eastern Europe",
        "Germany": "Western Europe",
        "Estonia": "Northern Europe",
        "Latvia": "Northern Europe",
        "Norway": "Northern Europe",
        "Sweden": "Northern Europe",
        "Finland": "Northern Europe",
        "Vietnam": "South-Eastern Asia",
        "Cambodia": "South-Eastern Asia",
        "Luxembourg": "Western Europe",
        "United Arab Emirates": "Western Asia",
        "Belgium": "Western Europe",
        "Georgia": "Western Asia",
        "North Macedonia": "Southern Europe",
        "Albania": "Southern Europe",
        "Azerbaijan": "Western Asia",
        "Kosovo": "Southern Europe",
        "Turkey": "Western Asia",
        "Spain": "Southern Europe",
        "Laos": "South-Eastern Asia",
        "Kyrgyzstan": "Central Asia",
        "Armenia": "Western Asia",
        "Denmark": "Northern Europe",
        "Libya": "Northern Africa",
        "Tunisia": "Northern Africa",
        "Romania": "Eastern Europe",
        "Hungary": "Eastern Europe",
        "Slovakia": "Eastern Europe",
        "Poland": "Eastern Europe",
        "Ireland": "Northern Europe",
        "United Kingdom": "Northern Europe",
        "Greece": "Southern Europe",
        "Zambia": "Eastern Africa",
        "Sierra Leone": "Western Africa",
        "Guinea": "Western Africa",
        "Liberia": "Western Africa",
        "Central African Republic": "Middle Africa",
        "Sudan": "Northern Africa",
        "Djibouti": "Eastern Africa",
        "Eritrea": "Eastern Africa",
        "Austria": "Western Europe",
        "Iraq": "Western Asia",
        "Italy": "Southern Europe",
        "Switzerland": "Western Europe",
        "Iran": "Southern Asia",
        "Netherlands": "Western Europe",
        "Liechtenstein": "Western Europe",
        "Ivory Coast": "Western Africa",
        "Republic of Serbia": "Southern Europe",
        "Mali": "Western Africa",
        "Senegal": "Western Africa",
        "Nigeria": "Western Africa",
        "Benin": "Western Africa",
        "Angola": "Middle Africa",
        "Croatia": "Southern Europe",
        "Slovenia": "Southern Europe",
        "Qatar": "Western Asia",
        "Saudi Arabia": "Western Asia",
        "Botswana": "Southern Africa",
        "Zimbabwe": "Southern Africa",
        "Pakistan": "Southern Asia",
        "Bulgaria": "Eastern Europe",
        "Thailand": "South-Eastern Asia",
        "San Marino": "Southern Europe",
        "Haiti": "Caribbean",
        "Dominican Republic": "Caribbean",
        "Chad": "Middle Africa",
        "Kuwait": "Western Asia",
        "El Salvador": "Central America",
        "Guatemala": "Central America",
        "East Timor": "South-Eastern Asia",
        "Brunei": "South-Eastern Asia",
        "Monaco": "Western Europe",
        "Algeria": "Northern Africa",
        "Mozambique": "Eastern Africa",
        "eSwatini": "Southern Africa",
        "Burundi": "Eastern Africa",
        "Rwanda": "Eastern Africa",
        "Myanmar": "South-Eastern Asia",
        "Bangladesh": "Southern Asia",
        "Andorra": "Southern Europe",
        "Afghanistan": "Southern Asia",
        "Montenegro": "Southern Europe",
        "Bosnia and Herzegovina": "Southern Europe",
        "Uganda": "Eastern Africa",
        "Cuba": "Caribbean",
        "Honduras": "Central America",
        "Ecuador": "South America",
        "Colombia": "South America",
        "Paraguay": "South America",
        "Portugal": "Southern Europe",
        "Moldova": "Eastern Europe",
        "Turkmenistan": "Central Asia",
        "Jordan": "Western Asia",
        "Nepal": "Southern Asia",
        "Lesotho": "Southern Africa",
        "Cameroon": "Middle Africa",
        "Gabon": "Middle Africa",
        "Niger": "Western Africa",
        "Burkina Faso": "Western Africa",
        "Togo": "Western Africa",
        "Ghana": "Western Africa",
        "Guinea-Bissau": "Western Africa",
        "United States of America": "Northern America",
        "Canada": "Northern America",
        "Mexico": "Central America",
        "Belize": "Central America",
        "Panama": "Central America",
        "Venezuela": "South America",
        "Papua New Guinea": "Melanesia",
        "Egypt": "Northern Africa",
        "Yemen": "Western Asia",
        "Mauritania": "Western Africa",
        "Equatorial Guinea": "Middle Africa",
        "Gambia": "Western Africa",
        "Hong Kong S.A.R.": "Eastern Asia",
        "Northern Cyprus": "Western Asia",
        "Australia": "Australia and New Zealand",
        "Greenland": "Northern America",
        "Fiji": "Melanesia",
        "New Zealand": "Australia and New Zealand",
        "Madagascar": "Eastern Africa",
        "Philippines": "South-Eastern Asia",
        "Sri Lanka": "Southern Asia",
        "The Bahamas": "Caribbean",
        "Taiwan": "Eastern Asia",
        "Japan": "Eastern Asia",
        "Iceland": "Northern Europe",
        "Seychelles": "Eastern Africa",
        "Kiribati": "Micronesia",
        "Marshall Islands": "Micronesia",
        "Trinidad and Tobago": "Caribbean",
        "Grenada": "Caribbean",
        "Saint Vincent and the Grenadines": "Caribbean",
        "Barbados": "Caribbean",
        "Saint Lucia": "Caribbean",
        "Dominica": "Caribbean",
        "Antigua and Barbuda": "Caribbean",
        "Saint Kitts and Nevis": "Caribbean",
        "Jamaica": "Caribbean",
        "Mauritius": "Eastern Africa",
        "Comoros": "Eastern Africa",
        "São Tomé and Principe": "Middle Africa",
        "Cabo Verde": "Western Africa",
        "Malta": "Southern Europe",
        "Singapore": "South-Eastern Asia",
        "Tonga": "Polynesia",
        "Samoa": "Polynesia",
        "Solomon Islands": "Melanesia",
        "Tuvalu": "Polynesia",
        "Maldives": "Southern Asia",
        "Nauru": "Micronesia",
        "Federated States of Micronesia": "Micronesia",
        "Vanuatu": "Melanesia",
        "Palau": "Micronesia",
        "Bahrain": "Western Asia",
        "Macao S.A.R": "Eastern Asia"
    }
    print(gdf[gdf["name"].str.contains("Tom", case=False, na=False)]["name"].unique())

    # Add the region column using your mapping
    gdf["region"] = gdf["name"].map(country_to_region)

    gdf = gdf.drop(columns=["ISO3166-1-Alpha-3", "ISO3166-1-Alpha-2"])

    # rename columns to code and name
    gdf = gdf.rename(columns={"name": "country", "region": "region"})
    gdf["geometry"] = gdf["geometry"].buffer(0)

    gdf = simplify_geometry(gdf)

    # rename "country" values to what we want here
    country_rename_map = {
        "Macao S.A.R": "Macao",
        "Hong Kong S.A.R.": "Hong Kong",
        "United Republic of Tanzania": "Tanzania",
        "United States of America": "United States",
        "Republic of Serbia": "Serbia",
    }

    gdf["country"] = gdf["country"].replace(country_rename_map)


    inspect_gdf(gdf)
    plot_gdf(gdf)

    # filter to region contains "Europe" or country is Turkey
    gdf = gdf[
        gdf["region"].str.contains("Europe", case=False, na=False) |
        (gdf["country"].astype(str) == "Turkey")
    ]


    save_to_csv(gdf, "countries_europe.csv")
    save_geojson(gdf, "countries_europe.geojson")