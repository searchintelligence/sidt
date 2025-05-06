import json
import requests


class Grubhub:
    def __init__(self):
        self.auth = None
        self.refresh_auth()

    def refresh_auth(self):
        response = requests.post(
            "https://api-gtm.grubhub.com/auth",
            json={
                'brand': 'GRUBHUB',
                'client_id': 'beta_UmWlpstzQSFmocLy3h1UieYcVST',
                'device_id': 2091223838,
                'refresh_token': '43816b81-18fe-4e2e-9b84-b485ad519ea8',
            })
        self.auth = response.json()["session_handle"]["access_token"]

    def get_restaurants(self, lat, lon, page=1, results=None):

        if results is None:
            results = []

        response = requests.get(
            "https://api-gtm.grubhub.com/topics-gateway/v1/topic/content",
            params={
                "pageSource": "HOME",
                "topicSource": "search/listing",
                "applicationId": "web",
                "topicId": "8b13ddfc-29b0-4452-b943-fa79e5cceebf",
                "locationMode": "DELIVERY",
                "operationId": "6f2cb8f3-1d55-484c-a18f-5541bb0511e7",
                "position": page,
                "location": f"POINT({lon} {lat})",
                "parameter": [
                    f"location.wkt:POINT({lon} {lat})",
                    "locationMode:DELIVERY",
                    "radius:10"
                ],
                "geohash": "9vk1mc9t52k5"
            },
            headers={'authorization': f'Bearer {self.auth}'}
        )

        # print(f"{response.status_code}, {page} of {response.json()[
        #       "object"]["data"]["pagination"]["total_pages"]}, {len(results)} collected")

        if response.status_code == 401:
            self.refresh_auth()
            return self.get_restaurants(lat, lon, page, results)

        if response.status_code == 200:
            r = response.json()
            # return r["object"]["data"]["pagination"]["total_items"] if "total_items" in r["object"]["data"]["pagination"] else 0
            content = r["object"]["data"]["content"]
            for item in content:
                results.append({
                    "id": item["entity"]["restaurant_id"],
                    "name": item["entity"]["name"],
                    "address": item["entity"]["address"]["street_address"],
                    "city": item["entity"]["address"]["address_locality"],
                    "state": item["entity"]["address"]["address_region"],
                    "rating": item["entity"]["ratings"]["actual_rating_value"] if "actual_rating_value" in item["entity"]["ratings"] else 0,
                    "reviews": item["entity"]["ratings"]["rating_count"],
                })
            try:
                if r["object"]["data"]["pagination"]["total_pages"] > page:
                    self.get_restaurants(lat, lon, page + 1, results)
                else:
                    return results
            except:
                return results

        return results
    

    def get_restaurants2(self, lat, lon, page=1, results=None):

        if results is None:
            results = []

        response = requests.get(
            f"https://api-gtm.grubhub.com/restaurants/search/search_listing?orderMethod=delivery_or_pickup&locationMode=DELIVERY_OR_PICKUP&facetSet=seoBrowseV1&pageSize=36&hideHateos=true&searchMetrics=true&sorts=seo_default&facet=delivery_cities%3Ac7be38d9-0d9f-4ebc-b46d-b9f8e2278a4c&facet=brand_id_uncollapsed%3A&sortSetId=seoBrowse&countOmittingTimes=true&pageNum={page}",
            headers={
            'authorization': f'Bearer {self.auth}',
        })

        if response.status_code == 401:
            self.refresh_auth()
            return self.get_restaurants(lat, lon, page, results)

        if response.status_code == 200:
            r = response.json()
            content = r["results"]
            for item in content:
                results.append({
                    "id": item["restaurant_id"],
                    "name": item["name"],
                    "address": item["address"]["street_address"],
                    "city": item["address"]["address_locality"],
                    "state": item["address"]["address_region"],
                    "rating": item["ratings"]["actual_rating_value"] if "actual_rating_value" in item["ratings"] else 0,
                    "reviews": item["ratings"]["rating_count"],
                })
            if r["pager"]["total_pages"] > page:
                self.get_restaurants2(lat, lon, page + 1, results)
            else:
                return results

        return results
        


gh = Grubhub()
results = gh.get_restaurants2(
    lat="29.4246002",
    lon="-98.4951405",
)
# print(json.dumps(results, indent=2, ensure_ascii=False))
print(len(results))
