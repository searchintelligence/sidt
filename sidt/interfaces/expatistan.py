import json
import re
from bs4 import BeautifulSoup
import requests
from ..utils.api import make_request

def search_by_city(query: str):
    """
    Search for cities using a query string.

    Args:
        query (str): The query string to search for.

    Returns:
        list: A list of dictionaries containing the search results. Each dictionary
        contains the following keys: 'id', 'name', and 'country'.
    """
    results = []

    url = f"https://www.expatistan.com/ajax/autocomplete_city"
    r = requests.request("GET", url, params={"term": query}).json()

    for item in r:
        results.append({
            "id": item["handle"],
            "name": item["name"],
            "country": item["country_code"],
        })

    return results

def get_countries():
    """
    Retrieves a dictionary of countries and their corresponding codes from a remote URL.

    Returns:
        dict: A dictionary containing the countries and their codes.
    """
    url = "https://www.gstatic.com/charts/regioncoder/0//geocodes/countries_en.js"
    r = requests.request("GET", url).text
    pattern = re.compile(r'var results = ({.*?});', re.DOTALL)
    return json.loads(pattern.search(r).group(1))


def get_cost_of_living(id: str, currency: str = "USD") -> dict:
    """
    Retrieves the cost of living data for a specific country or city from Expatistan.

    Args:
        id (str): The ID of the country or city to retrieve the cost of living data for.
        currency (str, optional): The currency to use for the cost of living data. Defaults to "USD".

    Returns:
        dict: A dictionary containing the cost of living items and their corresponding prices.
    """
    items = {}

    if id.lower() in get_countries().keys():
        url = f"https://www.expatistan.com/cost-of-living/country/{id.lower().replace(' ', '-')}?currency={currency}"
    else:
        url = f"https://www.expatistan.com/cost-of-living/{id}?currency={currency}"

    r = requests.request("GET", url).text
    data = BeautifulSoup(r, "html.parser").find("table", {"class": "comparison single-city"})

    for item in data.find_all("tr"):
        try:
            name = item.find("td", {"class": "item-name"}).get_text().replace("\n", "").strip()
            price = item.find("td", {"class": "price"}).get_text().replace("\n", "").strip()
        except:
            continue
        items[name] = price
        
    return items