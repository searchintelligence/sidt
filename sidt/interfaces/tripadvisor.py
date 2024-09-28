import requests
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


def canada_cities():
    """
    Returns a dictionary containing the Canadian city IDs and their corresponding names.

    Returns:
        dict: A dictionary where the keys are the city IDs and the values are the city names.
    """
    with open('sidt/data/tripadvisor/canada_city_ids.json') as f:
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


def get_reviews(id: int, filter: str = "", page: int = 0, page_token: str = None):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    }

    json_data = [
        {
            'variables': {
                'pageName': 'Attraction_Review',
                'parameters': [
                    {
                        'key': 'geoId',
                        'value': '28970',
                    },
                    {
                        'key': 'detailId',
                        'value': f'{id}',
                    },
                    {
                        'key': 'offset',
                        'value': f'{page}*10',
                    },
                ],
                'route': {
                    'page': 'Attraction_Review',
                    'params': {
                        'geoId': 28970,
                        'detailId': id,
                        'offset': f'{page}*10',
                    },
                },
                'routingLinkBuilding': False,
            },
            'extensions': {
                'preRegisteredQueryId': '211573a2b002568c',
            },
        },
        {
            'variables': {
                'page': 'Attraction_Review',
                'pos': 'en-US',
                'parameters': [
                    {
                        'key': 'geoId',
                        'value': '28970',
                    },
                    {
                        'key': 'detailId',
                        'value': f'{id}',
                    },
                    {
                        'key': 'offset',
                        'value': f'{page}*10',
                    },
                ],
                'factors': [
                    'TITLE',
                    'META_DESCRIPTION',
                    'MASTHEAD_H1',
                    'MAIN_H1',
                    'IS_INDEXABLE',
                    'RELCANONICAL',
                ],
                'route': {
                    'page': 'Attraction_Review',
                    'params': {
                        'geoId': 28970,
                        'detailId': id,
                        'offset': f'{page}*10',
                    },
                },
                'currencyCode': 'USD',
            },
            'extensions': {
                'preRegisteredQueryId': '18d4572907af4ea5',
            },
        },
        {
            'variables': {
                'request': {
                    'tracking': {
                        'screenName': 'Attraction_Review',
                        'pageviewUid': '793661c3-d13c-4a03-93a9-772bdf4abbc1',
                    },
                    'routeParameters': {
                        'contentType': 'attraction',
                        'contentId': f'{id}',
                    },
                    'clientState': {
                        'userInput': [
                            {
                                'inputKey': 'query',
                                'inputValues': [
                                    filter,
                                ],
                            },
                        ],
                    },
                    'updateToken': page_token,
                },
                'commerce': {},
                'sessionId': '27F62741D8B194DDE8EBFE2FC99E53F3',
                'tracking': {
                    'screenName': 'Attraction_Review',
                    'pageviewUid': '793661c3-d13c-4a03-93a9-772bdf4abbc1',
                },
                'currency': 'USD',
                'currentGeoPoint': None,
                'unitLength': 'MILES',
            },
            'extensions': {
                'preRegisteredQueryId': '390d68407a85dd79',
            },
        },
        {
            'variables': {
                'page': 'Attraction_Review',
                'params': [
                    {
                        'key': 'geoId',
                        'value': '28970',
                    },
                    {
                        'key': 'detailId',
                        'value': f'{id}',
                    },
                    {
                        'key': 'offset',
                        'value': f'{page}*10',
                    },
                ],
                'route': {
                    'page': 'Attraction_Review',
                    'params': {
                        'geoId': 28970,
                        'detailId': id,
                        'offset': f'{page}*10',
                    },
                },
            },
            'extensions': {
                'preRegisteredQueryId': 'f742095592a84542',
            },
        },
        {
            'variables': {
                'page': 'Attraction_Review',
                'locale': 'en-US',
                'platform': 'tablet',
                'id': f'{id}',
            },
            'extensions': {
                'preRegisteredQueryId': 'd194875f0fc023a6',
            },
        },
    ]

    response = make_request(
        method='POST',
        url='https://www.tripadvisor.com/data/graphql/ids',
        headers=headers,
        json=json_data).json()

    reviews = []
    sections = response[2]["data"]["Result"][0]["detailSectionGroups"][0]["detailSections"][0]["tabs"][0]["content"]
    for section in sections:
        if section["__typename"] == "WebPresentation_ReviewCardWeb":
            reviews.append({
                "id": json.loads(section["trackingKey"]).get("rid", None),
                "heading": section["htmlTitle"]["text"],
                "body": section["htmlText"]["text"],
                "rating": section["bubbleRatingNumber"],
            })

    next_page_token = None
    try:
        footer = response[2]["data"]["Result"][0]["detailSectionGroups"][0]["detailSections"][0]["tabs"][0]["content"][12]["links"]
        for link in footer:
            if int(link["pageNumber"]) == page+2:
                next_page_token = link["updateLink"]["updateToken"]
    except:
        pass

    if next_page_token:
        reviews.extend(get_reviews(id, filter, page+1, next_page_token))
    return reviews


def get_reviews_2(id: int, filter: str = "", page: int = 0, page_token: str = None):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    }

    json_data = [
        {
            'variables': {
                'pageName': 'Restaurant_Review',
                'relativeUrl': '/Restaurant_Review-g187147-d12714552-Reviews-or15-Pizzeria_Arrivederci-Paris_Ile_de_France.html',
                'parameters': [
                    {
                        'key': 'geoId',
                        'value': '187147',
                    },
                    {
                        'key': 'detailId',
                        'value': '12714552',
                    },
                    {
                        'key': 'offset',
                        'value': 'r15',
                    },
                ],
                'route': {
                    'page': 'Restaurant_Review',
                    'params': {
                        'geoId': 187147,
                        'detailId': 12714552,
                        'offset': 'r15',
                    },
                },
                'routingLinkBuilding': False,
            },
            'extensions': {
                'preRegisteredQueryId': '211573a2b002568c',
            },
        },
        {
            'variables': {
                'page': 'Restaurant_Review',
                'pos': 'en-US',
                'parameters': [
                    {
                        'key': 'geoId',
                        'value': '187147',
                    },
                    {
                        'key': 'detailId',
                        'value': '12714552',
                    },
                    {
                        'key': 'offset',
                        'value': 'r15',
                    },
                ],
                'factors': [
                    'TITLE',
                    'META_DESCRIPTION',
                    'MASTHEAD_H1',
                    'MAIN_H1',
                    'IS_INDEXABLE',
                    'RELCANONICAL',
                ],
                'route': {
                    'page': 'Restaurant_Review',
                    'params': {
                        'geoId': 187147,
                        'detailId': 12714552,
                        'offset': 'r15',
                    },
                },
                'currencyCode': 'USD',
            },
            'extensions': {
                'preRegisteredQueryId': '18d4572907af4ea5',
            },
        },
        {
            'variables': {
                'routesRequest': [
                    {
                        'fragment': '',
                        'page': 'Restaurant_Review',
                        'params': {
                            'geoId': 187147,
                            'detailId': 12714552,
                            'offset': 0,
                        },
                    },
                    {
                        'fragment': '',
                        'page': 'Restaurant_Review',
                        'params': {
                            'geoId': 187147,
                            'detailId': 12714552,
                            'offset': 'r30',
                        },
                    },
                ],
            },
            'extensions': {
                'preRegisteredQueryId': '3f2df7139a71a643',
            },
        },
        {
            'variables': {
                'locationId': 12714552,
                'offset': 15,
                'limit': 15,
                'keywordVariant': 'location_keywords_v2_llr_order_30_en',
                'needKeywords': True,
                'userId': 'A39E4BE820E927B2F7855C178DCFE52B',
                'filters': [
                    {
                        'axis': 'LANGUAGE',
                        'selections': [
                            'en',
                        ],
                    },
                    {
                        'axis': 'SORT',
                        'selections': [
                            'mostRecent',
                        ],
                    },
                    {
                        'axis': 'TEXT',
                        'selections': [
                            'good',
                        ],
                    },
                ],
                'prefs': {
                    'showMT': True,
                    'sortBy': 'DATE',
                    'sortType': '',
                },
                'initialPrefs': {
                    'showMT': True,
                    'sortBy': 'DATE',
                    'sortType': '',
                },
                'filterCacheKey': 'locationReviewsFilters_12714552',
                'prefsCacheKey': 'locationReviewsPrefs_12714552',
            },
            'extensions': {
                'preRegisteredQueryId': 'cbe12b7ea5ddf39c',
            },
        },
        {
            'variables': {
                'page': 'Restaurant_Review',
                'params': [
                    {
                        'key': 'geoId',
                        'value': '187147',
                    },
                    {
                        'key': 'detailId',
                        'value': '12714552',
                    },
                    {
                        'key': 'offset',
                        'value': 'r15',
                    },
                ],
                'route': {
                    'page': 'Restaurant_Review',
                    'params': {
                        'geoId': 187147,
                        'detailId': 12714552,
                        'offset': 'r15',
                    },
                },
            },
            'extensions': {
                'preRegisteredQueryId': 'f742095592a84542',
            },
        },
        {
            'variables': {
                'page': 'Restaurant_Review',
                'locale': 'en-US',
                'platform': 'desktop',
                'id': '12714552',
                'urlRoute': '/Restaurant_Review-g187147-d12714552-Reviews-or15-Pizzeria_Arrivederci-Paris_Ile_de_France.html',
            },
            'extensions': {
                'preRegisteredQueryId': 'd194875f0fc023a6',
            },
        },
    ]

    response = make_request(
        method='POST',
        url='https://www.tripadvisor.com/data/graphql/ids',
        headers=headers,
        json=json_data).json()

    reviews = []
    sections = response[2]["data"]["Result"][0]["detailSectionGroups"][0]["detailSections"][0]["tabs"][0]["content"]
    for section in sections:
        if section["__typename"] == "WebPresentation_ReviewCardWeb":
            reviews.append({
                "id": json.loads(section["trackingKey"]).get("rid", None),
                "heading": section["htmlTitle"]["text"],
                "body": section["htmlText"]["text"],
                "rating": section["bubbleRatingNumber"],
            })

    next_page_token = None
    try:
        footer = response[2]["data"]["Result"][0]["detailSectionGroups"][0]["detailSections"][0]["tabs"][0]["content"][12]["links"]
        for link in footer:
            if int(link["pageNumber"]) == page+2:
                next_page_token = link["updateLink"]["updateToken"]
    except:
        pass

    if next_page_token:
        reviews.extend(get_reviews(id, filter, page+1, next_page_token))
    return reviews
