from bs4 import BeautifulSoup
from ..utils.api import make_request

def make_search(query: str):
    results = []

    url = f"https://www.expatistan.com/ajax/autocomplete_city"
    params = {"term": query}
    r = make_request(url, params=params).json()

    for item in r:
        results.append({
            "id": item["handle"],
            "name": item["name"],
            "country": item["country_code"],
        })

    return results

def get_cost_of_living(city_id: str):
    items = {}

    url = f"https://www.expatistan.com/cost-of-living/{city_id}"
    r = make_request(url).text
    data = BeautifulSoup(r, "html.parser").find("table", {"class": "comparison single-city"})

    for item in data.find_all("tr"):
        try:
            name = item.find("td", {"class": "item-name"}).get_text().replace("\n", "").strip()
            price = item.find("td", {"class": "price"}).get_text().replace("\n", "").strip()
        except:
            continue
        items[name] = price
        
    return items