import json
from bs4 import BeautifulSoup
import requests


class Metacritic:
    def __init__(self):
        self.api_key = "1MOZgmNFxvmljaQR1X9KAij9Mo4xAY3u"

    def search(self, query: str):
        r = requests.get(f"https://internal-prod.apigee.fandom.net/v1/xapi/finder/metacritic/autosuggest/{query}?apiKey={self.api_key}")
        if r.status_code != 200:
            return None
        return r.json()["data"]

    def get_game(self, game_slug):
        r = requests.get(
            url=f"https://www.metacritic.com/game/{game_slug}/",
            headers={
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
            })
        if r.status_code != 200:
            return None
        soup = BeautifulSoup(r.text, "html.parser")
        data = json.loads(soup.find(attrs={"data-hid": "ld+json"}).text)
        return data