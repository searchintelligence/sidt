import json
import math
import re
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

def get_posts(username: str):
    posts = []
    more = True
    cursor = "null"
    while more:
        url = "https://www.instagram.com/graphql/query"
        payload = f'variables=%7B%22after%22%3A%22{cursor}%22%2C%22before%22%3Anull%2C%22data%22%3A%7B%22count%22%3A100%2C%22include_relationship_info%22%3Atrue%2C%22latest_besties_reel_media%22%3Atrue%2C%22latest_reel_media%22%3Atrue%7D%2C%22first%22%3A12%2C%22last%22%3Anull%2C%22username%22%3A%22{username}%22%2C%22__relay_internal__pv__PolarisFeedShareMenurelayprovider%22%3Afalse%7D&doc_id=8249268901750838'
        headers = {'content-type': 'application/x-www-form-urlencoded'}

        r = requests.request("POST", url, headers=headers, data=payload).json()["data"]["xdt_api__v1__feed__user_timeline_graphql_connection"]
        # return requests.request("POST", url, headers=headers, data=payload).json()

        cursor = r["page_info"]["end_cursor"]
        more = r["page_info"]["has_next_page"]
        for post in r["edges"]:
            post = post["node"]
            try: caption = post["caption"]["text"]
            except: caption = None
            posts.append({
                "id": post["id"],
                "caption": caption,
                "comment_count": post["comment_count"],
                "like_count": post["like_count"],
            })

    if posts: return {
        "info": {
            "posts_collected": len(posts),
            "average_likes": sum([post["like_count"] for post in posts]) / len(posts),
            "average_comments": sum([post["comment_count"] for post in posts]) / len(posts),
        },
        "posts": posts
    }
    else: return {
        "info": {
            "posts_collected": None,
            "average_likes": None,
            "average_comments": None,
        },
        "posts": posts
    }

# def get_profile_info(username: str):
#     headers = {
#         'X-IG-App-ID': '936619743392459',
#     }
#     url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}"
#     r = requests.request("GET", url, headers=headers).json()["data"]["user"]
#     profile = {
#             "name": r["full_name"],
#             "biography": r["biography"],
#             "followers": r["edge_followed_by"]["count"],
#             "following": r["edge_follow"]["count"],
#             "posts": r["edge_owner_to_timeline_media"]["count"],
#         }
    
#     return {
#         "profile": profile,
#         "calculations": {
#             "estimated_reach": None,
#             "estimated_story_impressions": None,
#             "estimated_post_impressions": None,
#             "engagement_rate": None,
#             "engagement_rate_benchmark": None,
#         },
#     }

def get_profile_info(username: str):
    url = "https://www.instagram.com/graphql/query"
    id = get_profile_id(username)

    payload = f'variables=%7B%22id%22%3A%22{id}%22%2C%22render_surface%22%3A%22PROFILE%22%7D&doc_id=7663723823674585'
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    headers = {
        'accept': '*/*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/x-www-form-urlencoded',
        # 'cookie': 'mid=ZcCo9gAEAAGPAQvjs5_cokvzF5WS; ig_did=218D31D4-EAA0-4DF9-B7DC-43207A701E29; datr=_6jAZV_jg2kfhfWWRhYCZhb8; fbm_124024574287414=base_domain=.instagram.com; ds_user_id=64879496178; oo=v1; csrftoken=t5UtQA9UnDuhFwIPIDdn1hYDdTfpQjVD; dpr=1; sessionid=64879496178%3ANPvOaY1pDUpnkd%3A23%3AAYf9hjpAeMJG5COJRQPaZv5CD5cYKXCQxhMzUB4Axg; rur="CLN\\05464879496178\\0541750332629:01f73197d141f156dd75c37cb312a586c1f174aa3af2fe77f8e1cd6495a0fc1ac562573a"; wd=317x1335',
        'dnt': '1',
        'origin': 'https://www.instagram.com',
        'priority': 'u=1, i',
        'referer': 'https://www.instagram.com/nasa/',
        'sec-ch-prefers-color-scheme': 'light',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126"',
        'sec-ch-ua-full-version-list': '"Not/A)Brand";v="8.0.0.0", "Chromium";v="126.0.6478.57"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"macOS"',
        'sec-ch-ua-platform-version': '"14.2.1"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'x-asbd-id': '129477',
        'x-bloks-version-id': 'e2004666934296f275a5c6b2c9477b63c80977c7cc0fd4b9867cb37e36092b68',
        'x-csrftoken': 't5UtQA9UnDuhFwIPIDdn1hYDdTfpQjVD',
        'x-fb-friendly-name': 'PolarisProfilePageContentDirectQuery',
        'x-fb-lsd': 'IGXtEmHBx6Y1M0olriQEnI',
        'x-ig-app-id': '936619743392459',
    }
    cookies = {
        'mid': 'ZcCo9gAEAAGPAQvjs5_cokvzF5WS',
        'ig_did': '218D31D4-EAA0-4DF9-B7DC-43207A701E29',
        'datr': '_6jAZV_jg2kfhfWWRhYCZhb8',
        'fbm_124024574287414': 'base_domain=.instagram.com',
        'ds_user_id': '64879496178',
        'oo': 'v1',
        'csrftoken': 't5UtQA9UnDuhFwIPIDdn1hYDdTfpQjVD',
        'dpr': '1',
        'sessionid': '64879496178%3ANPvOaY1pDUpnkd%3A23%3AAYf9hjpAeMJG5COJRQPaZv5CD5cYKXCQxhMzUB4Axg',
        'rur': '"CLN\\05464879496178\\0541750332629:01f73197d141f156dd75c37cb312a586c1f174aa3af2fe77f8e1cd6495a0fc1ac562573a"',
        'wd': '317x1335',
    }

    # return requests.request("POST", url, headers=headers, data=payload, cookies=cookies).json()

    r = requests.request("POST", url, headers=headers, data=payload, cookies=cookies).json()["data"]["user"]

    profile = {
            "name": r["full_name"],
            "biography": r["biography"],
            "followers": r["follower_count"],
            "following": r["following_count"],
            "posts": r["media_count"],
        }
    
    return {
        "profile": profile,
        "calculations": {
            "estimated_reach": None,
            "estimated_story_impressions": None,
            "estimated_post_impressions": None,
            "engagement_rate": None,
            "engagement_rate_benchmark": None,
        },
    }

def get_profile_id(username: str):
    url = "https://www.instagram.com/ajax/bulk-route-definitions/"

    payload = f'route_urls%5B0%5D=%2F{username}%2F&routing_namespace=igx_www&__d=www&__user=0&__a=1&__req=6&__hs=19893.HYP%3Ainstagram_web_pkg.2.1..0.1&dpr=2&__ccg=UNKNOWN&__rev=1014332205&__s=au2vlw%3A2q9cf3%3A1bg4i6&__hsi=7382196004816884148&__dyn=7xeUjG1mxu1syUbFp40NonwgU7SbzEdF8aUco2qwJxS0k24o0B-q1ew65xO0FE2awpUO0n24oaEnxO1ywOwv89k2C1Fwc60D87u3ifK0EUjwGzEaE2iwNwKwHw8Xxm16wUwtEvw4JwJCwLyES1TwVwDwHg2ZwrUdUbGwmk0zU8oC1Iwqo5q3e3zhA6bwIDyUrAwHyokxK3OqcyU-2K&__csr=hq2AdMNshNcWkp5qv948mP4EQ-8EyJ9LWkHRuWA9gCWmuroWKAZaBjhtKiicbQBigjAh9kGLheLGbGKiil4BCIEyl3bVoBaqaBLKialBF5yFKUJfwCz-UyAVGgCECh4y9ppkqbDAxmidy8VpokCJe2-ex-00kDJ2E0Y5wUw9Z2Unx61IwbC1Hg4ww0kvw1N5Wx51joG1opreCcg_Elgd8sz41IxGq0hl122p0EzQ0abw23yzo9A1hw5MzVE43w2--0Bo4O15w08ZO&__comet_req=7&fb_dtsg=NAcPhHJOBw1tjWL4RkQEYEiBT0R0_u52IC1MPMNMe28TS4lZvQf9iOA%3A17854477105113577%3A1713887019&jazoest=25906&lsd=U5yEIvpZgRmxm_vRtrYRzf&__spin_r=1014332205&__spin_b=trunk&__spin_t=1718801447&qpl_active_flow_ids=25305590'
    headers = {
    'accept': '*/*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'content-type': 'application/x-www-form-urlencoded',
    'cookie': 'mid=ZcCo9gAEAAGPAQvjs5_cokvzF5WS; ig_did=218D31D4-EAA0-4DF9-B7DC-43207A701E29; datr=_6jAZV_jg2kfhfWWRhYCZhb8; fbm_124024574287414=base_domain=.instagram.com; ds_user_id=64879496178; oo=v1; csrftoken=t5UtQA9UnDuhFwIPIDdn1hYDdTfpQjVD; dpr=1; sessionid=64879496178%3ANPvOaY1pDUpnkd%3A23%3AAYf9hjpAeMJG5COJRQPaZv5CD5cYKXCQxhMzUB4Axg; rur="CLN\\05464879496178\\0541750332928:01f7dfd4e07d933aa5224248836b92ca8cfa0678fcfdd09df7d518cd9ec76452d4cc8397"; wd=405x1335; csrftoken=t5UtQA9UnDuhFwIPIDdn1hYDdTfpQjVD; ds_user_id=64879496178; ig_did=F02710B3-4F18-4585-98D8-20932F244818; mid=ZnKy7QAEAAH1Yf_zXCw-e3Juky6K; rur="CLN\\05464879496178\\0541750329121:01f760fb0277bda994502d25e7f9ae6d2cb116afd58e26ecea3f9cda0b4bb32ad281b70e"; sessionid=64879496178%3ANPvOaY1pDUpnkd%3A23%3AAYdsR_yQQnG_Ngx8SEcYEkGhndGpXEcR9zlevpVtTw',
    'dnt': '1',
    'origin': 'https://www.instagram.com',
    'priority': 'u=1, i',
    'referer': 'https://www.instagram.com/nasa/',
    'sec-ch-prefers-color-scheme': 'light',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126"',
    'sec-ch-ua-full-version-list': '"Not/A)Brand";v="8.0.0.0", "Chromium";v="126.0.6478.57"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"macOS"',
    'sec-ch-ua-platform-version': '"14.2.1"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'x-asbd-id': '129477',
    'x-fb-lsd': 'U5yEIvpZgRmxm_vRtrYRzf',
    'x-fb-qpl-active-flows': '25305590',
    'x-ig-d': 'www'
    }

    # return requests.request("POST", url, headers=headers, data=payload, cookies=cookies).text
    r = requests.request("POST", url, headers=headers, data=payload).text
    return re.search(r'"profile_id":"(\d+)"', r).group(1)


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
    try:
        name = soup.find(class_="profile-name-bottom").get_text()
    except:
        name = None
    try:
        bio = soup.find(
            class_="profile-description").get_text().replace("\n", "").strip()
    except:
        bio = None
    try:
        posts = soup.find(class_="total_posts").get_text()
    except:
        posts = None
    try:
        followers = soup.find(class_="followed_by").get_text().replace(",", "")
    except:
        followers = None
    try:
        following = soup.find(class_="follows").get_text().replace(",", "")
    except:
        following = None
    try:
        stats = soup.find(
            class_="statistics-wrapper").find_all(recursive=False)
        avg_post_likes = stats[0].find(
            class_="profile-statistics__block-stat").get_text().replace("\n", "").strip()
        avg_post_comments = stats[1].find(
            class_="profile-statistics__block-stat").get_text().replace("\n", "").strip()
        time_between_posts = stats[2].find(
            class_="profile-statistics__block-stat").get_text().replace("\n", "").strip()
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
