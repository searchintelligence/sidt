import json
from math import ceil
from operator import ne
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

def get_review_overview2(id:str):
    cookies = {
        'SOCS': 'CAESHAgCEhJnd3NfMjAyNDEwMDMtMF9SQzEaAmVuIAEaBgiAj5e4Bg',
        'HSID': 'AIFOaK6KXnemx7g_l',
        'SSID': 'AO7894-RLvclfl9jx',
        'APISID': '0TRupispBieiBO4g/Aj50ulu_oto6YczIe',
        'SAPISID': 'y4680TbuX7rnmQBP/A2bow1D7Fp2OXPSUj',
        '__Secure-1PAPISID': 'y4680TbuX7rnmQBP/A2bow1D7Fp2OXPSUj',
        '__Secure-3PAPISID': 'y4680TbuX7rnmQBP/A2bow1D7Fp2OXPSUj',
        'S': 'maestro=Yg0pBMhiKfa0P6P0TUDR9TaRREcF4hJ7axKW9-aGCc8',
        'SID': 'g.a000wAg7mR4vE4EF3Bhk0aZI_A5K5KwK9xBLz4ybHgfpe9P883XDLKZ7RDv6_HouO7jXWk3vwgACgYKAT8SARASFQHGX2Mio7TtY7fjXJmEKJGpUUJOHhoVAUF8yKr0BFCpM9Y7cCOR39p-v6Hp0076',
        '__Secure-1PSID': 'g.a000wAg7mR4vE4EF3Bhk0aZI_A5K5KwK9xBLz4ybHgfpe9P883XDQ828V18m_xOfLvxG0e6wYwACgYKAWkSARASFQHGX2MiTBQR1N4Z4KiBodeC2CmIRxoVAUF8yKp4oFBRdpMHTatcZ_MHqS6c0076',
        '__Secure-3PSID': 'g.a000wAg7mR4vE4EF3Bhk0aZI_A5K5KwK9xBLz4ybHgfpe9P883XDqCszod3pjKeeWboNwC3u1gACgYKAToSARASFQHGX2MiKVpQlqIYhenPyZNBumZjHhoVAUF8yKpH9LdlUdju0O08cT3C0t8N0076',
        'NID': '523=cVfzHJMC8qMh7uea7W6ZWnVYdyRWD1P-A3f0H6sjIhvmBr-dNABH8VgqJM5nsbXsscQJMafW_fKM2FPafThzXIVecYAr4GvDR84PwGy1QMVoedqXrbZWQ_hNy_7lC6QZGZaeGtnyTYOfLgC78PecORDNjR14jCgc_WE_sOtYvmcMFQj6tzWnTqzZMc9J3UvlRZKN-mX0FmVb_XI9VJnt_0Mmqi5oQ4ILPEe256srWcw7rAdWhiL2v_cQXBZPgJZz_oLzusAmHLZa_59ECDLQkho-9tpVzeRgYCzT_-tHH41nxONlF7F9NHffND7WFzcutBvkif9z0rWwX7q1tyngTTlPoylaiWZpsTUcdax8Js9PUkImKIs1HelsyVnqeRkoKbisLWoLcqwbCSpAi9nZ3x9YhHMyf_9jXqw0g_XNZH-vec71m0BuvXKdNzDgXfpK2v9fPyDsWryUNi5BokRn7cQesEcpYkua2npx6DUO4_D74HMb2vOwzqfLlASAdAOmyo3uw-pJhTI2F0wK9phAXRhMZkDRGI1Ov_w9J2jpy7KKe16obBlKsmutmpHnjc18in0b8eJMr8BTbIEQvnkG8-Y6ymr0tQTGFqbPldu0gzyyHyjrBg0JOUJfLMGEGK0zR2EjCjqN2JTI0BEzJkv7XVkYQtDkszzJARypgqTugoUt-DqkUSOCRzsILnbUKc5b6cHPHd4pfMXkhEY9QfB55XUBg6iwRuCK_uDTBNdYcVo5jn1FR7_-T3kzr4zj1xX11xgfGC5Ve-PGmwM-dnIUotHOb0viTq0WErsKXUDVPR6_04AB7dzxCTw0DK1MwJJuab6jeiL8Z5ZyhcY9wVhp_Fv6l0tv70zadTe8FHwgvKHCcNGvZqmjGHHEZT-SSoMYshDzWLS2yfIV1U18KmXGfN93NWB-yWwVTEvTkdrn5MB0O__VW6meAOmvSW02zkRciwukIdCbK8WJoBXLKg8oEkityGlmv4Qu9uDtYBHfb2K-4dEH0COM4-dCUm3JMN2Vma5i83fFYvPqJDEuZJIRp4H-z9vNwQ9469q4BJy7nbrj8kG2ygQTfm7eAGSKu9JljQ',
        'AEC': 'AVcja2d45IRxLRl5QZ97P6OSNcGzuPnnECLrhJ1X_J2I8YZqlnma7grXOg',
        '__Secure-ENID': '27.SE=XBRgSHjMLSAiOsaO38d6Ul129JHHq33adCVbXcK-4JKjM-5SBW_UzEsgPPNu6LflgraSC6ZsZno0GYrpKN68UeCcIyZYtsnb7JWvjUCT0rhWSrkeOfcljnZTUpl8-kVpfy_6HdbhM9v6mereDc3jXXY6AVBOBjPsCEceIgECZ0--Tyjah3jGj9LP7UcY2ri_l1PsU7UE421Lx9LnznwofL0H8hFde6uLf_Lxo2NbPAOF0b5NUeFZ1Lc2y34us2X_ZSS1mKj24yOlIuCm_YkoKwEsbm67RN2f1UI4a0wmORIQFS_G0murXF29kWUIKtMCbhG6Xc7CZDQplHJNYRw9zBOyW0Ktc3Dl1MDtFJGpoAqb7Vhi2LCn9D8VoqGN0qspX0fv5uytm3e1T_mxeKkcUWQZZR79bEBCO8KoV3LxbQMxLctbdpHPY7olH4ceSNY5VuhZYolwhgY9Q6Dq6xIaygEC4UpZyE4GrI4',
        '__Secure-1PSIDTS': 'sidts-CjIB7pHptVCdVgeiZEBo-oYtakGPfCk7luhhrZEqjAgpHv2g03qsnlKI2N_WqxcriUShaxAA',
        '__Secure-3PSIDTS': 'sidts-CjIB7pHptVCdVgeiZEBo-oYtakGPfCk7luhhrZEqjAgpHv2g03qsnlKI2N_WqxcriUShaxAA',
        'DV': 'c82VJhmEX-0tYBSxunNAvzKTSBR7ZhkijpdIBVqZhgAAAAA',
        'SIDCC': 'AKEyXzVaX0cAs81-4-2hkqQJKTh8_c7NhOGjPUrMOeNGLqu6OeTaJg8tZWVC5V__IGeXSVxyRqk_',
        '__Secure-1PSIDCC': 'AKEyXzVaWMoXNLiBkKtItzCADgGxmYradNcceOfs7MsBxiQH18SOf_w2hz8jeqpN4Si6m-q1jqY',
        '__Secure-3PSIDCC': 'AKEyXzUh2v05srsuHNkJw3TnHRavtLWrDwyNxn24ThmPHXGW1uFdhmI14a1nnI_NgYvMYWGkUgw',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'dnt': '1',
        'downlink': '7.6',
        'origin': 'https://www.google.com',
        'priority': 'u=1, i',
        'referer': 'https://www.google.com/',
        'rtt': '100',
        'sec-ch-prefers-color-scheme': 'light',
        'sec-ch-ua': '"Chromium";v="135", "Not-A.Brand";v="8"',
        'sec-ch-ua-arch': '"arm"',
        'sec-ch-ua-bitness': '"64"',
        'sec-ch-ua-form-factors': '"Desktop"',
        'sec-ch-ua-full-version': '"135.0.7049.96"',
        'sec-ch-ua-full-version-list': '"Chromium";v="135.0.7049.96", "Not-A.Brand";v="8.0.0.0"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"macOS"',
        'sec-ch-ua-platform-version': '"15.4.1"',
        'sec-ch-ua-wow64': '?0',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        'x-client-data': 'CILvygE=',
        'x-client-pctx': 'CgcSBWjR7PMq',
        'x-same-domain': '1',
        # 'cookie': 'SOCS=CAESHAgCEhJnd3NfMjAyNDEwMDMtMF9SQzEaAmVuIAEaBgiAj5e4Bg; HSID=AIFOaK6KXnemx7g_l; SSID=AO7894-RLvclfl9jx; APISID=0TRupispBieiBO4g/Aj50ulu_oto6YczIe; SAPISID=y4680TbuX7rnmQBP/A2bow1D7Fp2OXPSUj; __Secure-1PAPISID=y4680TbuX7rnmQBP/A2bow1D7Fp2OXPSUj; __Secure-3PAPISID=y4680TbuX7rnmQBP/A2bow1D7Fp2OXPSUj; S=maestro=Yg0pBMhiKfa0P6P0TUDR9TaRREcF4hJ7axKW9-aGCc8; SID=g.a000wAg7mR4vE4EF3Bhk0aZI_A5K5KwK9xBLz4ybHgfpe9P883XDLKZ7RDv6_HouO7jXWk3vwgACgYKAT8SARASFQHGX2Mio7TtY7fjXJmEKJGpUUJOHhoVAUF8yKr0BFCpM9Y7cCOR39p-v6Hp0076; __Secure-1PSID=g.a000wAg7mR4vE4EF3Bhk0aZI_A5K5KwK9xBLz4ybHgfpe9P883XDQ828V18m_xOfLvxG0e6wYwACgYKAWkSARASFQHGX2MiTBQR1N4Z4KiBodeC2CmIRxoVAUF8yKp4oFBRdpMHTatcZ_MHqS6c0076; __Secure-3PSID=g.a000wAg7mR4vE4EF3Bhk0aZI_A5K5KwK9xBLz4ybHgfpe9P883XDqCszod3pjKeeWboNwC3u1gACgYKAToSARASFQHGX2MiKVpQlqIYhenPyZNBumZjHhoVAUF8yKpH9LdlUdju0O08cT3C0t8N0076; NID=523=cVfzHJMC8qMh7uea7W6ZWnVYdyRWD1P-A3f0H6sjIhvmBr-dNABH8VgqJM5nsbXsscQJMafW_fKM2FPafThzXIVecYAr4GvDR84PwGy1QMVoedqXrbZWQ_hNy_7lC6QZGZaeGtnyTYOfLgC78PecORDNjR14jCgc_WE_sOtYvmcMFQj6tzWnTqzZMc9J3UvlRZKN-mX0FmVb_XI9VJnt_0Mmqi5oQ4ILPEe256srWcw7rAdWhiL2v_cQXBZPgJZz_oLzusAmHLZa_59ECDLQkho-9tpVzeRgYCzT_-tHH41nxONlF7F9NHffND7WFzcutBvkif9z0rWwX7q1tyngTTlPoylaiWZpsTUcdax8Js9PUkImKIs1HelsyVnqeRkoKbisLWoLcqwbCSpAi9nZ3x9YhHMyf_9jXqw0g_XNZH-vec71m0BuvXKdNzDgXfpK2v9fPyDsWryUNi5BokRn7cQesEcpYkua2npx6DUO4_D74HMb2vOwzqfLlASAdAOmyo3uw-pJhTI2F0wK9phAXRhMZkDRGI1Ov_w9J2jpy7KKe16obBlKsmutmpHnjc18in0b8eJMr8BTbIEQvnkG8-Y6ymr0tQTGFqbPldu0gzyyHyjrBg0JOUJfLMGEGK0zR2EjCjqN2JTI0BEzJkv7XVkYQtDkszzJARypgqTugoUt-DqkUSOCRzsILnbUKc5b6cHPHd4pfMXkhEY9QfB55XUBg6iwRuCK_uDTBNdYcVo5jn1FR7_-T3kzr4zj1xX11xgfGC5Ve-PGmwM-dnIUotHOb0viTq0WErsKXUDVPR6_04AB7dzxCTw0DK1MwJJuab6jeiL8Z5ZyhcY9wVhp_Fv6l0tv70zadTe8FHwgvKHCcNGvZqmjGHHEZT-SSoMYshDzWLS2yfIV1U18KmXGfN93NWB-yWwVTEvTkdrn5MB0O__VW6meAOmvSW02zkRciwukIdCbK8WJoBXLKg8oEkityGlmv4Qu9uDtYBHfb2K-4dEH0COM4-dCUm3JMN2Vma5i83fFYvPqJDEuZJIRp4H-z9vNwQ9469q4BJy7nbrj8kG2ygQTfm7eAGSKu9JljQ; AEC=AVcja2d45IRxLRl5QZ97P6OSNcGzuPnnECLrhJ1X_J2I8YZqlnma7grXOg; __Secure-ENID=27.SE=XBRgSHjMLSAiOsaO38d6Ul129JHHq33adCVbXcK-4JKjM-5SBW_UzEsgPPNu6LflgraSC6ZsZno0GYrpKN68UeCcIyZYtsnb7JWvjUCT0rhWSrkeOfcljnZTUpl8-kVpfy_6HdbhM9v6mereDc3jXXY6AVBOBjPsCEceIgECZ0--Tyjah3jGj9LP7UcY2ri_l1PsU7UE421Lx9LnznwofL0H8hFde6uLf_Lxo2NbPAOF0b5NUeFZ1Lc2y34us2X_ZSS1mKj24yOlIuCm_YkoKwEsbm67RN2f1UI4a0wmORIQFS_G0murXF29kWUIKtMCbhG6Xc7CZDQplHJNYRw9zBOyW0Ktc3Dl1MDtFJGpoAqb7Vhi2LCn9D8VoqGN0qspX0fv5uytm3e1T_mxeKkcUWQZZR79bEBCO8KoV3LxbQMxLctbdpHPY7olH4ceSNY5VuhZYolwhgY9Q6Dq6xIaygEC4UpZyE4GrI4; __Secure-1PSIDTS=sidts-CjIB7pHptVCdVgeiZEBo-oYtakGPfCk7luhhrZEqjAgpHv2g03qsnlKI2N_WqxcriUShaxAA; __Secure-3PSIDTS=sidts-CjIB7pHptVCdVgeiZEBo-oYtakGPfCk7luhhrZEqjAgpHv2g03qsnlKI2N_WqxcriUShaxAA; DV=c82VJhmEX-0tYBSxunNAvzKTSBR7ZhkijpdIBVqZhgAAAAA; SIDCC=AKEyXzVaX0cAs81-4-2hkqQJKTh8_c7NhOGjPUrMOeNGLqu6OeTaJg8tZWVC5V__IGeXSVxyRqk_; __Secure-1PSIDCC=AKEyXzVaWMoXNLiBkKtItzCADgGxmYradNcceOfs7MsBxiQH18SOf_w2hz8jeqpN4Si6m-q1jqY; __Secure-3PSIDCC=AKEyXzUh2v05srsuHNkJw3TnHRavtLWrDwyNxn24ThmPHXGW1uFdhmI14a1nnI_NgYvMYWGkUgw',
    }

    params = {
        'rpcids': 'nz5PNe',
        'source-path': '/search',
        'hl': 'en-GB',
        '_reqid': '47196',
        'rt': 'c',
    }

    data = f'f.req=%5B%5B%5B%22nz5PNe%22%2C%22%5B%5B%5C%22{id}%5C%22%5D%2C1%5D%22%2Cnull%2C%22generic%22%5D%5D%5D&at=AKlEn5iJ1XLZHUGxLPYANZ_sMLag%3A1745496392870&'

    r = requests.post(
        'https://www.google.com/wizrpcui/_/WizRpcUi/data/batchexecute',
        params=params,
        cookies=cookies,
        headers=headers,
        data=data,
    )
    data1 = r.text.splitlines()[3:-2]
    data2 = json.loads('\n'.join(data1))
    data3 = json.loads(data2[0][2])
    review_count = data3[3]
    rating = data3[2]
    address = data3[1]
    return {
        "review_count": review_count,
        "rating": rating,
        "address": address
    }

def get_reviews2(id:str):

    reviews = []
    next_page_token = ""

    page_counter = 0
    more = True
    while more:
        try:
            url = f"https://www.google.com/maps/rpc/listugcposts?authuser=0&hl=en&gl=uk&pb=!1m6!1s{id}!6m4!4m1!1e1!4m1!1e3!2m2!1i10!2s{next_page_token}!5m2!1s2!7e81!8m9!2b1!3b1!5b1!7b1!12m4!1b1!2b1!4m1!1e1!11m0!13m1!1e1"
            r = requests.get(url, allow_redirects=True, headers=headers, cookies=cookies)
            data = json.loads(re.sub(r'^[^\[{]*', '', r.text))

            try: next_page_token = data[1]
            except: continue
            if next_page_token == "": more = False

            review_data = data[2]
            for item in review_data:
                try: author = item[0][1][4][5][0]
                except: author = None
                try: rating = 0
                except: rating = None
                try: date = item[0][1][6]
                except: date = None
                try: review = item[0][2][15][0][0]
                except: review = None
                reviews.append({
                    "author": author,
                    "rating": rating,
                    "date": date,
                    "review": review
                })
            page_counter += 1
        except:
            break
    if page_counter == 128: max_reached = True
    else: max_reached = False
    return {
        "max_reached": max_reached,
        "reviews_found": len(reviews),
        "pages": page_counter,
        "reviews": reviews
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
        r = requests.get(url, allow_redirects=True, headers=headers, cookies=cookies).text
        data = BeautifulSoup(r, "html.parser")

        try: next_page_token = data.find(attrs={"data-google-review-count":True}).get("data-next-page-token")
        except: continue
        if next_page_token == "": more = False

        print(f"next: {next_page_token}")

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