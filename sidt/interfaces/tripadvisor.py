from ..utils.api import make_request
import json

def us_states():
    """
    Returns a dictionary containing the US state IDs and their corresponding names.

    Returns:
        dict: A dictionary where the keys are the state IDs and the values are the state names.
    """
    with open('sidt/data/tripadvisor/us_state_ids.json') as f:
        return json.load(f)

def us_cities():
    """
    Returns a dictionary containing the US city IDs and their corresponding names.

    Returns:
        dict: A dictionary where the keys are the city IDs and the values are the city names.
    """
    with open('sidt/data/tripadvisor/us_city_ids.json') as f:
        return json.load(f)


def search(query: str, loc_types: list = None):
    """
    Search for locations on TripAdvisor based on the given query.

    Args:
        query (str): The search query.
        loc_types (list, optional): A list of location types to filter the search results. Defaults to All.

    Returns:
        list: A list of dictionaries containing information about the search results. Each dictionary contains the following keys:
            - id: The location ID.
            - name: The localized name of the location.
            - long_name: The localized additional names of the location.
            - latitude: The latitude of the location.
            - longitude: The longitude of the location.
            - type: The place type of the location.
    """
    if not loc_types:
        loc_types = get_location_types()
    results = []
    url = "https://www.tripadvisor.com/data/graphql/ids"
    payload = {
        "variables": {
            "request": {
                "query": query,
                "limit": 10,
                "scope": "WORLDWIDE",
                "locale": "en-US",
                "scopeGeoId": 1,
                "searchCenter": None,
                "types": [
                    "LOCATION",
                    "QUERY_SUGGESTION",
                    "RESCUE_RESULT"
                ],
                "locationTypes": loc_types,
            }
        },
        "extensions": {
            "preRegisteredQueryId": "50ad7bb9462525b2"
        }
    }
    r = make_request(url=url, method="POST", json=payload).json()
    for item in r["data"]["Typeahead_autocomplete"]["results"]:
        try:
            results.append({
                "id": item["locationId"],
                "name": item["details"]["localizedName"],
                "long_name": item["details"]["localizedAdditionalNames"]["longOnlyHierarchy"],
                "latitude": item["details"]["latitude"],
                "longitude": item["details"]["longitude"],
                "type": item["details"]["placeType"],
            })
        except KeyError:
            pass
    return results


def get_location_types():
    """
    Returns a list of all location types.

    Returns:
        list: A list of location types.
    """
    return [
        "GEO",
        "AIRPORT",
        "ACCOMMODATION",
        "ATTRACTION",
        "ATTRACTION_PRODUCT",
        "EATERY",
        "NEIGHBORHOOD",
        "AIRLINE",
        "SHOPPING",
        "UNIVERSITY",
        "GENERAL_HOSPITAL",
        "PORT",
        "FERRY",
        "CORPORATION",
        "VACATION_RENTAL",
        "SHIP",
        "CRUISE_LINE",
        "CAR_RENTAL_OFFICE"
    ]


def get_review_details(id: int):
    """
    Retrieves review details for a given location ID from TripAdvisor.

    Args:
        id (int): The location ID for which to retrieve review details.

    Returns:
        dict: A dictionary containing the review details, including the rating, number of reviews,
              rating aggregations, and language aggregations.
    """
    url = "https://www.tripadvisor.com/data/graphql/ids"
    payload = [
        {
            "variables": {
                "locationId": id,
                "keywordVariant": "location_keywords_v2_llr_order_30_en",
                "needKeywords": True,
                "prefs": {
                    "showMT": True,
                    "sortBy": "DATE",
                    "sortType": ""
                },
                "initialPrefs": {
                    "showMT": True,
                    "sortBy": "DATE",
                    "sortType": ""
                },
            },
            "extensions": {
                "preRegisteredQueryId": "793c8db508c1393b"
            }
        }
    ]
    r = make_request(method="POST", url=url, json=payload).json()

    return {
        "rating": r[-1]["data"]["locations"][0]["reviewSummary"]["rating"],
        "reviews": r[-1]["data"]["locations"][0]["reviewSummary"]["count"],
        "rating_aggregations": {
            "excelent": r[-1]["data"]["locations"][0]["reviewAggregations"]["ratingCounts"][4],
            "very_good": r[-1]["data"]["locations"][0]["reviewAggregations"]["ratingCounts"][3],
            "average": r[-1]["data"]["locations"][0]["reviewAggregations"]["ratingCounts"][2],
            "poor": r[-1]["data"]["locations"][0]["reviewAggregations"]["ratingCounts"][1],
            "terrible": r[-1]["data"]["locations"][0]["reviewAggregations"]["ratingCounts"][0],
        },
        "language_aggregations": r[-1]["data"]["locations"][0]["reviewAggregations"]["languageCounts"]
    }


def get_filtered_review_count(id: int, filter: str = ""):
    url = "https://www.tripadvisor.com/data/graphql/ids"
    payload = [
        {
            "variables": {
                "locationId": id,
                "keywordVariant": "location_keywords_v2_llr_order_30_en",
                "needKeywords": True,
                "filters": [
                    {
                        "axis": "TEXT",
                        "selections": [
                            filter
                        ]
                    }
                ],
                "prefs": {
                    "showMT": True,
                    "sortBy": "DATE",
                    "sortType": ""
                },
                "initialPrefs": {
                    "showMT": True,
                    "sortBy": "DATE",
                    "sortType": ""
                },
            },
            "extensions": {
                "preRegisteredQueryId": "793c8db508c1393b"
            }
        }
    ]
    r = make_request(method="POST", url=url, json=payload).json()
    return r[-1]["data"]["locations"][0]["reviewListPage"]["totalCount"]
