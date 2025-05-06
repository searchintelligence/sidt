import json
import requests


class Rightmove:

    def __init__(self):
        pass

    def get_loc_id(self, query):
        query = query.replace("-", " ")
        r = requests.get(
            url=f"https://los.rightmove.co.uk/typeahead?query={query}&limit=10&exclude=STREET",
        )
        if r.status_code != 200:
            return None

        data = r.json()["matches"][0]
        return {
            "location": data["displayName"],
            "id": data["id"]
        }

    def search(self, loc_id, type, index=0, results=None):
        if results is None:
            results = []

        r = requests.get(
            url="https://www.rightmove.co.uk/api/_search",
            params={
                "locationIdentifier": f"REGION^{loc_id}",
                "numberOfPropertiesPerPage": "500",
                "radius": "0.0",
                "sortType": "6", # 6=Newest 10=Oldest 2=Highest_Price 1=Lowest_Price
                "index": index,
                "includeLetAgreed": "false",
                "viewType": "LIST",
                "dontShow[0]": "retirement",
                "dontShow[1]": "sharedOwnership",
                "channel": type, # RENT or BUY
                "areaSizeUnit": "sqft",
                "currencyCode": "GBP",
                "isFetching": "false"
            }
        )
        data = r.json()

        expected = int(data["resultCount"].replace(",", ""))

        for property in data["properties"]:
            price, frequency = None, None
            if property["price"]["frequency"] == "weekly":
                price = property["price"]["amount"] * 4.33
                frequency = "monthly_calculated"
            results.append({
                "id": property["id"],
                "address": property["displayAddress"],
                "type": property["propertySubType"],
                "bedrooms": property["bedrooms"],
                "bathrooms": property["bathrooms"],
                "price": price if price else property["price"]["amount"],
                "price_frequency": frequency if frequency else property["price"]["frequency"],
            })
        
        if "next" in data["pagination"]:
            self.search(loc_id, type, data["pagination"]["next"], results)

        unique_results = {property['id']: property for property in results}
        unique_results = list(unique_results.values())
        return {
            "expected": expected,
            "scraped": len(unique_results),
            "results": unique_results
        }


# rm = Rightmove()
# search = rm.search("1403", "RENT")
# print(json.dumps(search, indent=2))
# print(len(search))
