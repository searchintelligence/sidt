import tls_client


class Tripadvisor:

    def __init__(self):
        self.client = tls_client.Session(random_tls_extension_order=True)

    def search(self, query: str, type: list[str] = None):

        if not type:
            type = ['GEO', 'AIRPORT', 'ACCOMMODATION', 'ATTRACTION', 'ATTRACTION_PRODUCT', 'EATERY', 'NEIGHBORHOOD', 'AIRLINE', 'SHOPPING',
                    'UNIVERSITY', 'GENERAL_HOSPITAL', 'PORT', 'FERRY', 'CORPORATION', 'VACATION_RENTAL', 'SHIP', 'CRUISE_LINE', 'CAR_RENTAL_OFFICE']

        r = self.client.post(
            url="https://www.tripadvisor.co.uk/data/graphql/ids",
            json=[
                {
                    'variables': {
                        'request': {
                            'query': query,
                            'limit': 20,
                            'scope': 'WORLDWIDE',
                            'locale': 'en-GB',
                            'scopeGeoId': 1,
                            'types': ['LOCATION'],
                            'locationTypes': type,
                        },
                        'userEngagedFilters': True
                    },
                    'extensions': {'preRegisteredQueryId': 'c2e5695e939386e4'},
                },
            ]
        )
        results = []
        for item in r.json()[0]["data"]["Typeahead_autocomplete"]["results"]:
            try:
                results.append({
                    "id": item["locationId"] if "locationId" in item else item["route"]["params"]["filters"][0]["value"][0],
                    "name": item["text"] if "text" in item else item["details"]["localizedName"],
                    "location": item["details"]["localizedAdditionalNames"]["longOnlyHierarchy"] if "details" in item else None,
                    "type": item["details"]["locationV2"]["placeType"] if "details" in item else item["buCategory"],
                })
            except:
                pass
        return results

    def get_hotels(self, geo_id: int, limit: int = None, style: list[int] = None):

        # todo: implement limit

        # STYLES:
        # 100  - Budget
        # 101  - Mid-range
        # 12   - Luxury
        # 4    - Family-friendly
        # 7    - Business
        # 3    - Romantic
        # 5951 - Modern

        results = []
        
        r = self.client.post(
            url="https://www.tripadvisor.co.uk/data/graphql/ids",
            json=[
                {
                    'variables': {
                        'geoId': geo_id,
                        'blenderId': None,
                        'currency': 'GBP',
                        'pricingMode': None,
                        'filters': {
                            'selectTravelersChoiceWinner': False,
                            'selectTravelersChoiceBOTBWinner': False,
                            'minRating': None,
                            'neighborhoodsOrNear': None,
                            'priceRange': None,
                            'amenities': None,
                            'brands': None,
                            'classes': None,
                            'styles': style,
                            'hoteltypes': None,
                            'categories': None,
                            'anyTags': None,
                            'hotelowners': None,
                        },
                        'offset': 0,
                        'limit': 750,
                        'sort': 'BEST_VALUE',
                        'clientType': 'DESKTOP',
                        'viewType': 'LIST',
                        'productId': "Hotels",
                        'pageviewId': '33333342-bd80-4cff-8343-366b579b5a35',
                        'sessionId': 'D5DE12A90395E45616ACB50CB3CA0B4D',
                        'userEngagedFilters': True,
                    },
                    'extensions': {'preRegisteredQueryId': '8bd4c19b6fddca69'}
                },
            ]
        )
        
        for item in r.json()[0]["data"]["list"]["results"]:
            if not item["resultDetail"]["hotelMetaResult"]["isFullMatch"]:
                # Skip items that don't fully match search filters
                continue
            try: id = item["locationId"]
            except: id = None
            try: name = item["location"]["locationV2"]["names"]["name"]
            except: name = None
            try: rating = item["location"]["reviewSummary"]["rating"]
            except: rating = None
            try: reviews = item["location"]["reviewSummary"]["count"]
            except: reviews = None
            try: lat = item["location"]["locationV2"]["geocode"]["latitude"]
            except: lat = None
            try: long = item["location"]["locationV2"]["geocode"]["longitude"]
            except: long = None
            results.append({"id": id, "name": name, "rating": rating, "reviews": reviews, "geo": {"lat": lat, "long": long}})
        return results