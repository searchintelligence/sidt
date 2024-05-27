import requests
from ..utils.api import make_request

cookies = {
    'ds_user_id': '64879496178',
    'sessionid': '64879496178%3ANPvOaY1pDUpnkd%3A23%3AAYeI0qYp2X93J_1kr1N8T-qRTwoMefBqtpiMqdYn3Q',
}

headers = {
    'X-IG-App-ID': '936619743392459',
}

def get_hashtag_popularity(tag):
    params = {"tag_name": tag}
    url = "https://www.instagram.com/api/v1/tags/web_info/"
    r = make_request(url=url, method="GET", headers=headers, cookies=cookies, params=params).json()
    try:
        return r["count"]
    except:
        return None

def get_profile_info(username):
    url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}"

    r = requests.request("GET", url, headers=headers).json()["data"]["user"]
    return {
        "follower_count": r["edge_followed_by"]["count"],
        "following_count": r["edge_follow"]["count"],
    }