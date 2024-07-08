import requests

class Instagram:

    # Api has a rate limit of 200 requests per hour

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.cookies = {'sessionid': self.session_id}
        self.headers = {'X-IG-App-ID': '936619743392459'}


    def get_profile_id(self, username: str):
        try:
            return int(self.make_search_query(username)["users"][0]["user"]["pk"])
        except:
            return 0
        
    def get_hashtag_popularity(self, tag: str):
        url = "https://www.instagram.com/api/v1/tags/web_info/"
        params = {"tag_name": tag}
        
        r = requests.get(url, headers=self.headers, cookies=self.cookies, params=params)
        if r.status_code == 404:
            return 0
        try:
            return r.json()["count"]
        except:
            raise Exception(f"Error finding data for #{tag}")

    def make_search_query(self, query: str):
        url = f"https://www.instagram.com/web/search/topsearch/?query={query}"

        r = requests.get(url, headers=self.headers, cookies=self.cookies)
        return r.json()

    def get_user_info(self, id: int):
        url = f'https://i.instagram.com/api/v1/users/{id}/info'

        r = requests.get(url, cookies=self.cookies, headers=self.headers)

        if r.status_code == 404:
            raise Exception("User not found")
        if r.json()["status"] != "ok":
            raise Exception(f"API returned with status \"{r.json()['status']}\": {r.json()['message']}")
        
        data = r.json()["user"]

        try: public_email = data["public_email"]
        except: public_email = None

        return {
            "id": id,
            "username": data["username"],
            "full_name": data["full_name"],
            "account_type": data["account_type"],
            "biography": data["biography"],
            "email": public_email,
            "followers": data["follower_count"],
            "following": data["following_count"],
            "posts": data["media_count"],
        }

    def get_user_feed(self, id: int, collect_all: bool = True):
        url = f'https://i.instagram.com/api/v1/feed/user/{id}/'
        max_id = None
        params = {"max_id": max_id, "count": 33}

        posts = []
        while True:
            r = requests.get(url, cookies=self.cookies, headers=self.headers, params=params)
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

    def generate_user_analysis(self, username: str):
        id = self.get_profile_id(username)
        info = self.get_user_info(id)
        posts = self.get_user_feed(id, collect_all=False)

        followers = info["followers"]
        following = info["following"]
        average_likes = sum([post["likes"] for post in posts]) / len(posts)
        average_comments = sum([post["comments"] for post in posts]) / len(posts)
        engagement_rate = (average_likes + average_comments) / followers * 100

        def get_base_cost(followers: int):
            if followers < 1000:
                return 10
            elif followers < 10000:
                return 25
            elif followers < 50000:
                return 20
            elif followers < 300000:
                return 15
            elif followers < 1000000:
                return 10
            else:
                return 0

        cost = get_base_cost(followers) + (followers / 100) * (1 + engagement_rate / 100)

        return{
            "followers": followers,
            "following": following,
            "posts": info["posts"],
            "sample_size": len(posts),
            "average_likes": average_likes,
            "average_comments": average_comments,
            "estimated_reach": None,
            "estimated_story_impressions": None,
            "estimated_post_impressions": None,
            "engagement_rate": engagement_rate,
            "engagement_rate_benchmark": None,
            "price_per_post": {
                "min": cost - (cost * 0.15),
                "max": cost + (cost * 0.15)
            }
        }