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
