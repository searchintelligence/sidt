import re
from bs4 import BeautifulSoup
import requests


class Steam:

    def __init__(self):
        self.url = "https://steamcommunity.com"
    
    def get_id_from_url(self, url: str):
        if "profiles" in url:
            return url.split("profiles/")[-1][:-1]
        elif "id" in url:
            return url.split("id/")[-1][:-1]
        else:
            return None

    def search_store(self, query: str):
        results = []
        params = {
            'term': query,
            'f': 'games',
            'cc': 'GB',
            'realm': '1',
            'l': 'english',
            'v': '24293162',
            # 'excluded_content_descriptors[]': [
            #     '3',
            #     '4',
            # ],
            'use_store_query': '1',
            'use_search_spellcheck': '1',
            'search_creators_and_tags': '1',
        }

        r = requests.get('https://store.steampowered.com/search/suggest', params=params)
        items = BeautifulSoup(r.text, "html.parser").find_all(class_="match")

        for item in items:

            try: id = item.get("data-ds-appid")
            except: id = None

            try: name = item.find(class_="match_name").get_text()
            except: name = None

            try: price = item.find(class_="match_subtitle").get_text()
            except: price = None

            try: image = item.find("img").get("src")
            except: image = None

            results.append({
                "id": id,
                "name": name,
                "price": price,
                "image": image,
            })
    
        return results


    def get_reviews(self, app_id: int, filter: str = "toprated", page: int = 1, cursor: str = None, max: int = None):

        # Benchmark for all CS2(id: 730) reviews = 9600 reviews in 12 minutes, max ~700MB of memory.

        reviews = []

        params = {
            'userreviewscursor': cursor,
            # 'userreviewsoffset': '20',
            'p': page,
            # 'workshopitemspage': page,
            # 'readytouseitemspage': page,
            # 'mtxitemspage': page,
            # 'itemspage': page,
            # 'screenshotspage': page,
            # 'videospage': page,
            # 'artpage': page,
            # 'allguidepage': page,
            # 'webguidepage': page,
            # 'integratedguidepage': page,
            # 'discussionspage': page,
            'numperpage': '10',
            'browsefilter': [
                filter,
                # 'toprated',
            ],
            'appHubSubSection': [
                '10',
                '10',
            ],
            'l': 'english',
            'filterLanguage': 'default',
            'searchText': '',
            'maxInappropriateScore': '100',
            'forceanon': '1',
        }

        r = requests.get(f"{self.url}/app/{app_id}/homecontent/", params=params)
        soup = BeautifulSoup(r.text, "html.parser")
        items = soup.find_all(class_="apphub_Card")

        for item in items:

            try:
                hours_played = item.find(class_="hours").get_text().replace(" hrs on record", "")
            except:
                hours_played = 0

            feedback = item.find('div', class_='found_helpful').get_text()
            try:
                helpful_match = re.search(r'(\d{1,3}(?:,\d{3})*) people found this review helpful', feedback)
                helpful = int(helpful_match.group(1).replace(',', ''))
            except:
                helpful = 0
            try:
                funny_match = re.search(r'(\d{1,3}(?:,\d{3})*) people found this review\s+funny', feedback)
                funny = int(funny_match.group(1).replace(',', ''))
            except:
                funny = 0
            
            date = item.find(class_="date_posted").get_text().replace("Posted: ", "")
            item.find(class_='date_posted').decompose()

            reviews.append({
                "title": item.find(class_="title").get_text(),
                "body": item.find(class_='apphub_CardTextContent').get_text(strip=True, separator=" "),
                "date": date,
                "author": {
                    "id": self.get_id_from_url(item.find(class_="apphub_CardContentAuthorName").find("a").get("href")),
                    "name": item.find(class_="apphub_CardContentAuthorName").get_text(),
                    "hours_played": hours_played,
                },
                "feedback": {
                    "helpful": helpful,
                    "funny": funny,
                    "awards": None,
                },
            })
        
        if max is None or len(reviews) < max:
            try:
                reviews.extend(self.get_reviews(
                    app_id = app_id,
                    filter = filter,
                    page = page + 1,
                    cursor = soup.find(attrs={"name": "userreviewscursor"}).get("value"),
                    max = max - len(reviews) if max is not None else None,
                    ))
            except:
                pass

        return reviews
