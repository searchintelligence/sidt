import requests
import random

def generate_session_id():
    tokens = [
        "64879496178%3ANPvOaY1pDUpnkd%3A23%3AAYdsR_yQQnG_Ngx8SEcYEkGhndGpXEcR9zlevpVtTw",
        "64879496178%3ANPvOaY1pDUpnkd%3A23%3AAYdPuPyB-PgKRzLznreqM60W0iY_z2p7Om-DCDY4nVQ"
    ]
    return random.choice(tokens)

def get_profile_id(username: str):
    try:
        return int(make_search_query(username)["users"][0]["user"]["pk"])
    except:
        raise Exception("User not found")

def make_search_query(query: str):
    url = f"https://www.instagram.com/web/search/topsearch/?query={query}"
    headers = {'X-IG-App-ID': '936619743392459'}
    cookies = {'sessionid': generate_session_id()}
    r = requests.get(url, headers=headers, cookies=cookies)
    return r.json()

def get_user_info(id: int):
    url = f'https://i.instagram.com/api/v1/users/{id}/info'
    headers = {'X-IG-App-ID': '936619743392459'}
    cookies = {'sessionid': generate_session_id()}

    r = requests.get(url, cookies=cookies, headers=headers)

    if r.status_code == 404:
        raise Exception("User not found")
    if r.json()["status"] != "ok":
        raise Exception(f"API returned with status \"{r.json()['status']}\": {r.json()['message']}")
    
    data = r.json()["user"]

    return {
        "id": id,
        "username": data["username"],
        "full_name": data["full_name"],
        "account_type": data["account_type"],
        "biography": data["biography"],
        "email": data["public_email"],
        "followers": data["follower_count"],
        "following": data["following_count"],
        "posts": data["media_count"],
    }

def get_user_feed(id: int, collect_all: bool = True):
    url = f'https://i.instagram.com/api/v1/feed/user/{id}/'
    headers = {'X-IG-App-ID': '936619743392459'}

    posts = []
    max_id = None
    while True:
        r = requests.get(url, cookies={'sessionid': generate_session_id()}, headers=headers, params = {"max_id": max_id, "count": 33})
        for item in r.json()["items"]:
            try: caption = item["caption"]["text"]
            except: caption = ""
            posts.append({
                "id": item["pk"],
                "type": item["media_type"],
                "caption": caption,
                "timestamp": item["taken_at"],
                "likes": item["like_count"],
                "comments": item["comment_count"],
            })
        if r.json()["more_available"] and collect_all:
            max_id = r.json()["next_max_id"]
        else:
            break

    return posts

def generate_user_analysis(username: str):
    id = get_profile_id(username)
    info = get_user_info(id)
    posts = get_user_feed(id, collect_all=False)

    followers = info["followers"]
    following = info["following"]
    average_likes = sum([post["likes"] for post in posts]) / len(posts)
    average_comments = sum([post["comments"] for post in posts]) / len(posts)
    return{
        "followers": followers,
        "following": following,
        "posts": info["posts"],
        "average_likes": average_likes,
        "average_comments": average_comments,
        "estimated_reach": (average_likes + average_comments) / followers * 100,
        "estimated_story_impressions": None,
        "estimated_post_impressions": None,
        "engagement_rate": None,
        "engagement_rate_benchmark": None,
    }