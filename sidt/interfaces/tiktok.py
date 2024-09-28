import requests


class Tiktok:
    def __init__(self):
        pass

    def get_hashtag_info(self, hashtag):

        data = requests.get(
            "https://www.tiktok.com/api/challenge/detail/",
            params={"challengeName": hashtag}
        ).json()

        return {
            "title": data["shareMeta"]["title"],
            "video_count": int(data["challengeInfo"]["statsV2"]["videoCount"]),
            "view_count": int(data["challengeInfo"]["statsV2"]["viewCount"]),
        }