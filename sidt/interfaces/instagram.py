from ..utils.utils import makeRequest

cookies = {
    'mid': 'ZcCo9gAEAAGPAQvjs5_cokvzF5WS',
    'ig_did': '218D31D4-EAA0-4DF9-B7DC-43207A701E29',
    'datr': '_6jAZV_jg2kfhfWWRhYCZhb8',
    'fbm_124024574287414': 'base_domain=.instagram.com',
    'ds_user_id': '64879496178',
    'oo': 'v1',
    'csrftoken': 't5UtQA9UnDuhFwIPIDdn1hYDdTfpQjVD',
    'sessionid': '64879496178%3ANPvOaY1pDUpnkd%3A23%3AAYeI0qYp2X93J_1kr1N8T-qRTwoMefBqtpiMqdYn3Q',
    'rur': '"CLN.05464879496178.0541745423647:01f7997bafaef853b3f0536302785099dae9b4580fec06a2130612d97b8667d842b2329c"',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-GB,en;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    # 'Cookie': 'mid=ZcDF3gALAAHmfgJO96XovjORkKIm; ig_did=70317F26-85E0-4B83-8CF1-9C3FBB2F6D89; csrftoken=eHBe4rL1S1EsrOAAl7OwozyuFJ0gBDOI; ds_user_id=64524236694; sessionid=64524236694%3AcGQ1qM0e57Cv6M%3A23%3AAYexHRr73v9UBjcuLd5eCinc_KABOee51AxEWNZr6A; rur="LDC\\05464524236694\\0541738668840:01f7e28ed22ee7618dd59f28bccc391e034fa18b0bdc651b31dc5c6607ff0cba7997a492"',
    'Origin': 'https://www.instagram.com',
    'Referer': 'https://www.instagram.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
    'X-ASBD-ID': '129477',
    'X-CSRFToken': 'eHBe4rL1S1EsrOAAl7OwozyuFJ0gBDOI',
    'X-FB-Friendly-Name': 'PolarisSearchBoxRefetchableQuery',
    'X-FB-LSD': 'gtXbdxrUwLwvlqrT0az3LS',
    'X-IG-App-ID': '936619743392459',
    'dpr': '1.5',
    'sec-ch-prefers-color-scheme': 'light',
    'sec-ch-ua': '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
    'sec-ch-ua-full-version-list': '"Not A(Brand";v="99.0.0.0", "Microsoft Edge";v="121.0.2277.83", "Chromium";v="121.0.6167.85"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"10.0.0"',
    'viewport-width': '1050',
}

def getHashtagPopularity(tag):
    params = {"tag_name": tag}
    url = "https://www.instagram.com/api/v1/tags/web_info/"
    r = makeRequest(url=url, method="GET", headers=headers, cookies=cookies, params=params).json()
    try:
        return r["count"]
    except:
        return "Error"
