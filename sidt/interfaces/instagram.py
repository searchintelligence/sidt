import math
from bs4 import BeautifulSoup
import requests
from ..utils.api import make_request

cookies = {
    'ds_user_id': '64879496178',
    'sessionid': '64879496178%3ANPvOaY1pDUpnkd%3A23%3AAYeI0qYp2X93J_1kr1N8T-qRTwoMefBqtpiMqdYn3Q',
}

headers = {
    'X-IG-App-ID': '936619743392459',
}


def get_hashtag_popularity(tag: str):
    params = {"tag_name": tag}
    url = "https://www.instagram.com/api/v1/tags/web_info/"
    r = make_request(url=url, method="GET", headers=headers,
                     cookies=cookies, params=params).json()
    try:
        return r["count"]
    except:
        return None


def get_profile_info(username: str):
    url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}"

    r = requests.request("GET", url, headers=headers).json()["data"]["user"]
    return {
        "follower_count": r["edge_followed_by"]["count"],
        "following_count": r["edge_follow"]["count"],
    }


def get_inzpire_data(username: str, currency: str = "EUR", posts: int = 1, stories: int = 1):
    url = "https://inzpire.me/api/v1/submit/calculate"
    try:
        r = requests.post(url=url, json={"username": username}).json()
    except:
        return {
            "followers": None,
            "total_posts": None,
            "estimated_reach": None,
            "estimated_story_impressions": None,
            "estimated_post_impressions": None,
            "engagement_rate": None,
            "engagement_rate_benchmark": None,
            "estimated_price": {
                "currency": None,
                "min": None,
                "max": None,
            }
        }

    conversion_rates = {
        "USD": 1.1738,
        "GBP": 0.854,
        "NOK": 10.194,
        "SEK": 10.1944,
        "DKK": 7.4357
    }

    def round_value(value, base): return math.floor(value / base) * base

    def estimated_reach(posts, stories, followers):
        if posts != 0:
            if followers < 20000:
                c = round(0.9489 * math.pow(followers, 0.92542))
            else:
                c = round(4.938 * math.pow(followers, 0.76593))
        else:
            c = 0

        if stories != 0:
            u = round(1.4626 * math.pow(followers, 0.7635))
        else:
            u = 0

        if posts > 0:
            return round_value(c, 100)
        elif stories > 0:
            return round_value(u, 100)
        else:
            return 0

    def engagement_rate_benchmark(followers):
        return round(0.6121 * math.pow(followers, 0.71861) / followers * 100, 1)

    def estimated_post_impressions(posts, followers):
        if posts != 0:
            return round_value(posts * (5.81215 * math.pow(followers, 0.76854)), 100)
        else:
            return 0

    def estimated_story_impressions(stories, followers):
        if stories != 0:
            return round_value(stories * (1.88168 * math.pow(followers, 0.75157)), 100)
        else:
            return 0

    def price_range(posts, stories, followers, currency):
        post_impressions = estimated_post_impressions(posts, followers)
        story_impressions = estimated_story_impressions(stories, followers)

        min_price = round_value(
            25 * (post_impressions + story_impressions) / 1000, 10) + 10
        max_price = round_value(
            30 * (post_impressions + story_impressions) / 1000, 10) + 10

        if currency in conversion_rates:
            min_price *= conversion_rates[currency]
            max_price *= conversion_rates[currency]

        return round(min_price), round(max_price)

    price_range = price_range(posts, stories, r["followers"], currency)

    return {
        "followers": r["followers"],
        "total_posts": r["totalPosts"],
        "estimated_reach": estimated_reach(posts, stories, r["followers"]),
        "estimated_story_impressions": estimated_story_impressions(stories, r["followers"]),
        "estimated_post_impressions": int(estimated_post_impressions(posts, r["followers"])),
        "engagement_rate": round(r["engagementRate"], 1),
        "engagement_rate_benchmark": engagement_rate_benchmark(r["followers"]),
        "estimated_price": {
            "currency": currency,
            "min": price_range[0],
            "max": price_range[1],
        }
    }


def get_picuki_data(username: str):
    url = f"https://www.picuki.com/profile/{username}"
    try:
        r = make_request(url=url, method="GET", persistant=False).text
    except:
        return {
            "name": None,
            "bio": None,
            "posts": None,
            "followers": None,
            "following": None,
            "avg_post_likes": None,
            "avg_post_comments": None,
            "time_between_posts": None
        }
    soup = BeautifulSoup(r, "html.parser")
    try: name = soup.find(class_="profile-name-bottom").get_text()
    except: name = None
    try: bio = soup.find(class_="profile-description").get_text().replace("\n", "").strip()
    except: bio = None
    try: posts = soup.find(class_="total_posts").get_text()
    except: posts = None
    try: followers = soup.find(class_="followed_by").get_text().replace(",", "")
    except: followers = None
    try: following = soup.find(class_="follows").get_text().replace(",", "")
    except: following = None
    try:
        stats = soup.find(class_="statistics-wrapper").find_all(recursive=False)
        avg_post_likes = stats[0].find(class_="profile-statistics__block-stat").get_text().replace("\n", "").strip()
        avg_post_comments = stats[1].find(class_="profile-statistics__block-stat").get_text().replace("\n", "").strip()
        time_between_posts = stats[2].find(class_="profile-statistics__block-stat").get_text().replace("\n", "").strip()
    except:
        avg_post_likes = None
        avg_post_comments = None
        time_between_posts = None
    return {
        "name": name,
        "bio": bio,
        "posts": posts,
        "followers": followers,
        "following": following,
        "avg_post_likes": avg_post_likes,
        "avg_post_comments": avg_post_comments,
        "time_between_posts": time_between_posts
    }