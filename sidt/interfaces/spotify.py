from dataclasses import dataclass
import requests
from sidt.utils.api import make_request

@dataclass
class Auth:
    client_id: str
    client_secret: str

base_url = "https://api.spotify.com/v1/"

def generate_bearer_token():
    from seleniumwire import webdriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    attempts = 0
    token = ""
    while True and attempts < 10:
        attempts += 1
        driver.get("https://open.spotify.com/track/5fZJQrFKWQLb7FpJXZ1g7K")
        for request in driver.requests:
            if "authorization" in request.headers.keys() and "Bearer" in request.headers['authorization']:
                token = request.headers['authorization']
        if token:
            return token       
    return None

def get_token(auth: Auth):
    # Generates bearer token valid for 1hr
    data = {
        "grant_type": "client_credentials",
        "client_id": auth.client_id,
        "client_secret": auth.client_secret,
    }
    return requests.post('https://accounts.spotify.com/api/token', data=data).json()["access_token"]

def get_album(uri: str):
    headers = {
        'authorization': generate_bearer_token(),
    }
    items = []
    url = f"https://api-partner.spotify.com/pathfinder/v1/query?operationName=queryAlbumTracks&variables=%7B%22uri%22%3A%22{uri}%22%2C%22offset%22%3A0%2C%22limit%22%3A300%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%22469874edcad37b7a379d4f22f0083a49ea3d6ae097916120d9bbe3e36ca79e9d%22%7D%7D"
    r = make_request(url=url, method="GET", headers=headers).json()
    for i in r["data"]["albumUnion"]["tracks"]["items"]:
        items.append({
            "name": i["track"]["name"],
            "uri": i["track"]["uri"],
            "plays": i["track"]["playcount"],
        })
    return items

def get_track(uri:str, auth: generate_bearer_token):
    headers = {
        'authorization': auth,
    }
    
    url = url = f"https://api-partner.spotify.com/pathfinder/v1/query?operationName=getTrack&variables=%7B%22uri%22%3A%22{uri}%22%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%22ae85b52abb74d20a4c331d4143d4772c95f34757bfa8c625474b912b9055b5c0%22%7D%7D"
    return make_request(url=url, method="GET", headers=headers).json()["data"]["trackUnion"]["playcount"]