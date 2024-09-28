from math import ceil
import re
from bs4 import BeautifulSoup
import requests

cookies = {
    'SEARCH_SAMESITE': 'CgQIkpoB',
    'HSID': 'AqeqpxJw6ZQnLxz29',
    'SSID': 'AubeqvvRl_A4N0YCb',
    'APISID': 'IJq09C1w-3ZkH9XV/AqF1k16Cxwwj2i5LA',
    'SAPISID': '7SwvL8CFmPvHZ4mK/AOxRBQOi2iewtFeyR',
    '__Secure-1PAPISID': '7SwvL8CFmPvHZ4mK/AOxRBQOi2iewtFeyR',
    '__Secure-3PAPISID': '7SwvL8CFmPvHZ4mK/AOxRBQOi2iewtFeyR',
    '__Secure-1PSIDTS': 'sidts-CjIBPVxjSk0er6eG80MeCdVASVnwfte_5Bf6Fwl9Tnn7useF36j2vTj1KV2drvcOkKU0ZxAA',
    '__Secure-3PSIDTS': 'sidts-CjIBPVxjSk0er6eG80MeCdVASVnwfte_5Bf6Fwl9Tnn7useF36j2vTj1KV2drvcOkKU0ZxAA',
    'S': 'billing-ui-v3=XyZVGPUUqai_EpvAR7ovekix161vXLwF:billing-ui-v3-efe=XyZVGPUUqai_EpvAR7ovekix161vXLwF:maestro=xbVlHURwgRRqXiqSDvFWeuDSCb2HRSNgK8TavrzW3EE',
    'NID': '513=A-Bmzu_L6BH-jKfidx-tbOt43c14_8JwcZEXBY-rUUInDbV7-h6eqMe5Ppk8jetMW7uDaXDOn8Foy9UJ5Kk12-3ldMWlv5KPvbBIQ4rJC8Y3La1tUgm1CrnaJ5COPN5k5jkk8aZTjUf185HqUXIqrked6QPKJc3YqPqPG53XuyIcTW7p_C_ZZXzrT08ULTzYDY8FFMehGGQtRIouMR21JdJJpOG3tUceTPrWRnq40yO1XJ2KUGpcIfhPjRttUevxPg8mi4DnJ0G4sMdI3X2Wpf0r9Hc',
    'SID': 'g.a000kAg7mRTq1YqrZbt45XyUBd4e8Gf7aoxZP4RvWt6yh-V4kycCBmz6YIOkGcVfdYnyMv4zGgACgYKAf8SAQASFQHGX2MiHk8ZcWbtEpE0fScp1uMtiBoVAUF8yKoEAei1SetULJOrmuIWrE-p0076',
    '__Secure-1PSID': 'g.a000kAg7mRTq1YqrZbt45XyUBd4e8Gf7aoxZP4RvWt6yh-V4kycCZV-zKElYwXN8RvkR8Nhr8QACgYKATcSAQASFQHGX2MiLSCf0_4TuZLuOwcgLXUFjhoVAUF8yKpYHuk_ZhceRaQ0XZ2x5Y4P0076',
    '__Secure-3PSID': 'g.a000kAg7mRTq1YqrZbt45XyUBd4e8Gf7aoxZP4RvWt6yh-V4kycCTUGNYFFrmx4ABE4QJAOVIwACgYKAfISAQASFQHGX2Miy1Gw0Ap6ma6HI4xYYTE3ghoVAUF8yKrWDMKGqwuKxaYz9eUXMdk_0076',
    'OTZ': '7576568_52_56_123900_52_436380',
    'AEC': 'AQTF6HxAd_HIIpioB-fglusrtITfdxeLW4rryL-I0C6u175wyvsTRsbyjg',
    '__Secure-ENID': '19.SE=gv60eEh67dC7HUyEyxTZpNWfVxi-qlPtmEHBc_4eBDmGOkoJiOKL9pPGDIZge3xHMDw3NEE-s6A6VZ86ZRo2IM-4ZwHOY--zUjYGHtyIEaQsQjASsGz7fFGy126iS8g4JGpqT3QQX8jXm0wlqjmdUbr2L1f49zSlgQC7GyPNRkEKU8HvtpagXuasNH3GGwcyMZG2NUfibRciQLr2qmqfyi7g0p2PQ428_i2Vy6BrerhT9R3qSeN_S7_lkPRgi4PythM8yD6P7hNQq9ZBo0Wd8irOJGxgg1CsVux94lN5F3r3R-l5yrB3GCiu2XeP9_TlHpyBdv-2QQqBqiM_iiD2jFabd8_Ho6dIOpKKyH3KeLgyUe1e8ns1C7BgnwudJkN27hM0g0r_R4RgNlUOKuH_Fg',
    'GOOGLE_ABUSE_EXEMPTION': 'ID=e80183eea3ae30c2:TM=1716983847:C=r:IP=86.30.34.80-:S=xchMqzBNAJLGZROroKpurlg',
    'DV': 'c82VJhmEX-0tYBSxunNAvzIjLmZD_BgijpdIBVqZBgAAAAA',
    'SIDCC': 'AKEyXzVw0VUhlUprXCcYALLLbodT3m5SZnbvGqK6nVEyRuws9AMeiJFeikcstfY6MaEZ2Gm3fUk',
    '__Secure-1PSIDCC': 'AKEyXzUl9TVoCnePCyPbTA3_N4M0cqKuvuT_MwmF5uJrynzirogiRYxy_J3gIK_Hus8F5euCHzJc',
    '__Secure-3PSIDCC': 'AKEyXzX4Egq9N2X-MDjo5msdNtkVFt-LvqEV2YGn9CG-CKQehZ9BuVo8xSXVxDJPPEa0piBwfwQ',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    # 'cookie': 'SEARCH_SAMESITE=CgQIkpoB; HSID=AqeqpxJw6ZQnLxz29; SSID=AubeqvvRl_A4N0YCb; APISID=IJq09C1w-3ZkH9XV/AqF1k16Cxwwj2i5LA; SAPISID=7SwvL8CFmPvHZ4mK/AOxRBQOi2iewtFeyR; __Secure-1PAPISID=7SwvL8CFmPvHZ4mK/AOxRBQOi2iewtFeyR; __Secure-3PAPISID=7SwvL8CFmPvHZ4mK/AOxRBQOi2iewtFeyR; __Secure-1PSIDTS=sidts-CjIBPVxjSk0er6eG80MeCdVASVnwfte_5Bf6Fwl9Tnn7useF36j2vTj1KV2drvcOkKU0ZxAA; __Secure-3PSIDTS=sidts-CjIBPVxjSk0er6eG80MeCdVASVnwfte_5Bf6Fwl9Tnn7useF36j2vTj1KV2drvcOkKU0ZxAA; S=billing-ui-v3=XyZVGPUUqai_EpvAR7ovekix161vXLwF:billing-ui-v3-efe=XyZVGPUUqai_EpvAR7ovekix161vXLwF:maestro=xbVlHURwgRRqXiqSDvFWeuDSCb2HRSNgK8TavrzW3EE; NID=513=A-Bmzu_L6BH-jKfidx-tbOt43c14_8JwcZEXBY-rUUInDbV7-h6eqMe5Ppk8jetMW7uDaXDOn8Foy9UJ5Kk12-3ldMWlv5KPvbBIQ4rJC8Y3La1tUgm1CrnaJ5COPN5k5jkk8aZTjUf185HqUXIqrked6QPKJc3YqPqPG53XuyIcTW7p_C_ZZXzrT08ULTzYDY8FFMehGGQtRIouMR21JdJJpOG3tUceTPrWRnq40yO1XJ2KUGpcIfhPjRttUevxPg8mi4DnJ0G4sMdI3X2Wpf0r9Hc; SID=g.a000kAg7mRTq1YqrZbt45XyUBd4e8Gf7aoxZP4RvWt6yh-V4kycCBmz6YIOkGcVfdYnyMv4zGgACgYKAf8SAQASFQHGX2MiHk8ZcWbtEpE0fScp1uMtiBoVAUF8yKoEAei1SetULJOrmuIWrE-p0076; __Secure-1PSID=g.a000kAg7mRTq1YqrZbt45XyUBd4e8Gf7aoxZP4RvWt6yh-V4kycCZV-zKElYwXN8RvkR8Nhr8QACgYKATcSAQASFQHGX2MiLSCf0_4TuZLuOwcgLXUFjhoVAUF8yKpYHuk_ZhceRaQ0XZ2x5Y4P0076; __Secure-3PSID=g.a000kAg7mRTq1YqrZbt45XyUBd4e8Gf7aoxZP4RvWt6yh-V4kycCTUGNYFFrmx4ABE4QJAOVIwACgYKAfISAQASFQHGX2Miy1Gw0Ap6ma6HI4xYYTE3ghoVAUF8yKrWDMKGqwuKxaYz9eUXMdk_0076; OTZ=7576568_52_56_123900_52_436380; AEC=AQTF6HxAd_HIIpioB-fglusrtITfdxeLW4rryL-I0C6u175wyvsTRsbyjg; __Secure-ENID=19.SE=gv60eEh67dC7HUyEyxTZpNWfVxi-qlPtmEHBc_4eBDmGOkoJiOKL9pPGDIZge3xHMDw3NEE-s6A6VZ86ZRo2IM-4ZwHOY--zUjYGHtyIEaQsQjASsGz7fFGy126iS8g4JGpqT3QQX8jXm0wlqjmdUbr2L1f49zSlgQC7GyPNRkEKU8HvtpagXuasNH3GGwcyMZG2NUfibRciQLr2qmqfyi7g0p2PQ428_i2Vy6BrerhT9R3qSeN_S7_lkPRgi4PythM8yD6P7hNQq9ZBo0Wd8irOJGxgg1CsVux94lN5F3r3R-l5yrB3GCiu2XeP9_TlHpyBdv-2QQqBqiM_iiD2jFabd8_Ho6dIOpKKyH3KeLgyUe1e8ns1C7BgnwudJkN27hM0g0r_R4RgNlUOKuH_Fg; DV=c82VJhmEX-0tgIjjJVKBVqYBqFdB_JhRxOrOAf3KzAAAAAA; SIDCC=AKEyXzVq3m7ttMnh2UzBMSVoxGGH3pCgSsqiCiE3ZG_WolTeRGWoHCft5zVS7BUmlCWpZfZqTUo; __Secure-1PSIDCC=AKEyXzVw6JVImmBkkb5ZxS1QY3CSi4MnLiXqVuN6Yg3QbkYCcVvsEdEMB79dPMTgvmfba5tmuCa0; __Secure-3PSIDCC=AKEyXzUh1_5m2aD8GFqBUWWU48k5_RZAoKZ9cWNLptRFqN-Ekqz654qaCwZzvxvJ68N8vo08TVo',
    'dnt': '1',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-arch': '"arm"',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-full-version': '"125.0.6422.112"',
    'sec-ch-ua-full-version-list': '"Chromium";v="125.0.6422.112", "Not.A/Brand";v="24.0.0.0"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"macOS"',
    'sec-ch-ua-platform-version': '"14.2.1"',
    'sec-ch-ua-wow64': '?0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'x-client-data': 'CI+NywE=',
}

def get_id(search:str):
    # Requires headers and cookies, is slow, triggers captcha, requires cookie reset after captcha
    url = f"https://www.google.com/search?q={search}"
    r = requests.request("GET", url, cookies=cookies, headers=headers).text
    try:
        return BeautifulSoup(r, "html.parser").find(attrs={"data-async-trigger": "reviewDialog"}).get("data-fid")
    except:
        return None


def get_review_overview(id:str):
    url = f"https://www.google.com/async/reviewDialog?async=feature_id:{id},sort_by:qualityScore,_fmt:pc"
    r = requests.request("GET", url).text
    data = BeautifulSoup(r, "html.parser")
    review_count = int(data.find(class_="z5jxId").get_text().split(" ")[0].replace(",", ""))
    rating = float(data.find(class_="Aq14fc").get_text())
    address = data.find(class_="ffUfxe").get_text()
    return {
        "review_count": review_count,
        "rating": rating,
        "address": address
    }

def get_reviews(id:str, sort_by:str="qualityScore"):
    valid_sort_options = ["qualityScore", "newestFirst", "ratingHigh", "ratingLow"]
    if sort_by not in valid_sort_options:
        raise ValueError(f"Invalid sort_by value. Must be one of: {', '.join(valid_sort_options)}")

    reviews = []
    next_page_token = ""

    page_counter = 0
    more = True
    while more:

        url = f"https://www.google.com/async/reviewDialog?async=feature_id:{id},sort_by:{sort_by},next_page_token:{next_page_token},_fmt:pc"
        r = requests.request("GET", url, allow_redirects=True, headers=headers, cookies=cookies).text
        data = BeautifulSoup(r, "html.parser")

        try: next_page_token = data.find(attrs={"data-google-review-count":True}).get("data-next-page-token")
        except: continue
        if next_page_token == "": more = False

        review_data = data.find(attrs={"data-google-review-count": True}).find_all(attrs={"jscontroller": "fIQYlf"})

        for item in review_data:
            try: author = item.find(class_="TSUbDb").get_text()
            except: author = None
            try: rating = re.search(r'Rated (\d\.\d) out of 5', item.find(class_="lTi8oc z3HNkc").get("aria-label")).group(1)
            except: rating = None
            try: date = item.find(class_="dehysf").get_text()
            except: date = None
            try: review = item.find(attrs={"data-expandable-section": True}).get_text()
            except: review = None
            reviews.append({
                "author": author,
                "rating": rating,
                "date": date,
                "review": review
            })
        page_counter += 1
    if page_counter == 128: max_reached = True
    else: max_reached = False
    return {
        "max_reached": max_reached,
        "reviews_found": len(reviews),
        "pages": page_counter,
        "reviews": reviews
    }

def temp(id:str):
    next_page_token = ""
    count = 0
    while True:
        try:
            url = f"https://www.google.com/async/reviewDialog?async=feature_id:{id},sort_by:qualityScore,next_page_token:{next_page_token},_fmt:pc"
            r = requests.request("GET", url, allow_redirects=True, headers=headers, cookies=cookies).text
            data = BeautifulSoup(r, "html.parser")
            next_page_token = data.find(attrs={"data-google-review-count":"10"}).get("data-next-page-token")
            if next_page_token == "": break
            print(next_page_token)
            count += 1
        except: break
    print(count)