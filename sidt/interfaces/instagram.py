import time
from xml.dom import NotFoundErr
import requests
import tls_client


class Instagram:

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.cookies = {'sessionid': self.session_id}
        self.headers = {'X-IG-App-ID': '936619743392459'}
        self.client = tls_client.Session(random_tls_extension_order=True)

    def get_profile_id(self, username: str, helper: str = ''):
        try:
            users = self.make_search_query(
                username)['data']['xdt_api__v1__fbsearch__topsearch_connection']['users']
            for user in users:
                if user["user"]["username"] == username:
                    return int(user["user"]["pk"])
        except:
            return 0
        return 0

    def make_search_query(self, query: str):
        client = tls_client.Session(
            client_identifier="chrome128",
            random_tls_extension_order=True
        )
        data = {
            'av': '17841464805349937',
            '__d': 'www',
            '__user': '0',
            '__a': '1',
            '__req': '2t',
            '__hs': '20136.HYP:instagram_web_pkg.2.1...1',
            'dpr': '2',
            '__ccg': 'EXCELLENT',
            '__rev': '1020163651',
            '__s': 'vlb1x6:grad8d:fmuwdh',
            '__hsi': '7472415572494576442',
            '__dyn': '7xeUjG1mxu1syUbFp41twpUnwgU7SbzEdF8aUco2qwJxS0DU2wx609vCwjE1EE2Cw8G11wBz81s8hwGxu786a3a1YwBgao6C0Mo2iyo7u3ifK0EUjwGzEaE2iwNwmE2eUlwhEe87q0oa2-azqwt8d-2u2J0bS1LwTwKG1pg2fwxyo6O1FwlEcUed6goK2O4Xxui2qi7E5y4UrwHwcObBK4o',
            '__csr': 'gR1xd3cZgTNsQYZFsBdAkGBjGCiQmGiLBqhAFlKAW-vXAgF1d5TVAmFltquul4HiAAK-8KFrVqCpaAZ5LIBLF5hGx_G9p9m8BAAhpvnF4Dt29qDyVufAxim4LDy_jCCBzkA9hK-VazEF9oy8QhohQ9J5wABwyK8GiVUCGyF9e00jCF4Au0HU4KqpkkiXoG0hu3e5ohx11fxuGwoS0hi0AU8o3xw6uwoE0Ta0hW0aIjc0QpGl154yBxi7Wg9kOjxm685Wt0b3wuC6ia8IG28CO09-awJAwG2esg1dxq13yo9E7ylm5Q8U7deh0NEE6um1m40a-8w1bOp2pE05RCU0-m0bow',
            '__comet_req': '7',
            'fb_dtsg': 'NAcPLYnUswr9JiZtH-eFmwAkmaF9bDwZH3Vy0jnc6DtEqK-ZyERHBvQ:17865068956001195:1739363773',
            'jazoest': '26338',
            'lsd': 'dSGCoZGsWnwOzynGVbgQcJ',
            '__spin_r': '1020163651',
            '__spin_b': 'trunk',
            '__spin_t': '1739807327',
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'PolarisSearchBoxRefetchableQuery',
            'variables': '{"data":{"context":"blended","include_reel":"true","query":"' + query + '","rank_token":"","search_surface":"web_top_search"},"hasQuery":true}',
            'server_timestamps': 'true',
            'doc_id': '8964418863643891',
        }

        r = client.post('https://www.instagram.com/graphql/query', data=data)
        return r.json()

    def get_hashtag_popularity(self, tag: str):
        return self.get_hashtag_popularity_graphql(tag)

    def get_hashtag_popularity_graphql(self, tag: str):

        tag = tag.replace(" ", "").lower()

        r = self.client.post(
            url="https://www.instagram.com/graphql/query",
            headers={"content-type": "application/x-www-form-urlencoded"},
            data={'variables': '{"data":{"query":"#'+tag+'"},"hasQuery":true}','doc_id': '28955733317403314'}
        )

        if r.status_code != 200:
            time.sleep(1)
            return self.get_hashtag_popularity_graphql(tag)

        for item in r.json()["data"]["xdt_api__v1__fbsearch__topsearch_connection"]["hashtags"]:
            if item["hashtag"]["name"] == tag:
                return item["hashtag"]["media_count"]
            
            
        return 0

    def get_user_info(self, id: int):
        url = f'https://i.instagram.com/api/v1/users/{id}/info'

        r = requests.get(url, cookies=self.cookies, headers=self.headers)

        if r.status_code == 404:
            raise NotFoundErr("User not found")
        if r.json()["status"] != "ok":
            raise Exception(
                f"API returned with status \"{r.json()['status']}\": {r.json()['message']}")

        data = r.json()["user"]

        try:
            public_email = data["public_email"]
        except:
            public_email = None

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
            r = requests.get(url, cookies=self.cookies,
                             headers=self.headers, params=params)
            for item in r.json()["items"]:
                try:
                    caption = item["caption"]["text"]
                except:
                    caption = ""
                posts.append({
                    "id": item["pk"],
                    "type": item["media_type"],
                    "caption": caption,
                    "timestamp": item["taken_at"],
                    "likes": item["like_count"],
                    "comments": item["comment_count"],
                })
            try:
                if r.json()["more_available"] and collect_all:
                    max_id = r.json()["next_max_id"]
                else:
                    break
            except:
                break

        return posts

    def generate_user_analysis(self, username: str, helper: str = ''):
        id = self.get_profile_id(username, helper)
        info = self.get_user_info(id)
        posts = self.get_user_feed(id, collect_all=False)

        followers = info["followers"]
        following = info["following"]
        average_likes = sum([post["likes"] for post in posts]) / \
            len(posts) if len(posts) > 0 else 0
        average_comments = sum(
            [post["comments"] for post in posts]) / len(posts) if len(posts) > 0 else 0
        engagement_rate = (average_likes + average_comments) / \
            followers * 100 if followers > 0 else 0

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

        cost = get_base_cost(followers) + (followers / 100) * \
            (1 + engagement_rate / 100)

        return {
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

    def find_user(self, user: str):
        candidates = []
        search = self.make_search_query(user)
        for item in search['users']:
            candidates.append({
                'pk': item['user']['pk'],
                'username': item['user']['username'],
                'position': item['position'],
                'name': item['user']['full_name'],
                'verified': item['user']['is_verified'],
                'followers': self.get_user_feed(item['user']['pk'])['followers']
            })
        return candidates
