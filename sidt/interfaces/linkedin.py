from dataclasses import dataclass
import json
from math import ceil
from bs4 import BeautifulSoup
from ..utils.api import make_request
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'cookie': 'bcookie="v=2&e82ebc5d-1bef-4179-83a3-6edf5fa48ca0"; bscookie="v=1&202401291344235525765f-c0c0-4be2-866e-31c85a20f2b9AQEl9FsOpgx8oJzLLlotw--j2lV7iCqe"; li_alerts=e30=; g_state={"i_p":1709728539658,"i_l":1}; li_gc=MTs0MjsxNzA5NzIxMzQ5OzI7MDIxrfVE0dRYq4gexXFCdcjjXUxXijQJUel7wWRmMA+VPoA=; timezone=Europe/London; li_theme=light; li_theme_set=app; dfpfpt=ca1dec89dac34463bb1839e36d3a3587; PLAY_LANG=en; PLAY_SESSION=eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjp7InNlc3Npb25faWQiOiIzMzU2YTAwMy1iZmE2LTQ0NDUtYmU1NC1mODA5NWRmMTNkYWJ8MTcxNDk4OTE0MSIsImFsbG93bGlzdCI6Int9IiwicmVjZW50bHktc2VhcmNoZWQiOiIiLCJyZWZlcnJhbC11cmwiOiJodHRwczovL3d3dy5saW5rZWRpbi5jb20vaGVscC9saW5rZWRpbi9hbnN3ZXIvYTcyMDAxOT9saXBpPXVybiUzQWxpJTNBcGFnZSUzQWRfZmxhZ3NoaXAzX3Byb2ZpbGVfc2VsZl9lZGl0X3RvcF9jYXJkJTNCb2dMUHIyNDdSU0d5c3JkUXBwSGFnZyUzRCUzRCIsInJlY2VudGx5LXZpZXdlZCI6IiIsIkNQVC1pZCI6IsKNXHTCvyfCjTFcdTAwMTAuw7E3worCsWzCgz_DjiIsImV4cGVyaWVuY2UiOiIiLCJ0cmsiOiIifSwibmJmIjoxNzE0OTg5MTQxLCJpYXQiOjE3MTQ5ODkxNDF9.ZTP3uqTII-rxQhWPaPgfq2toAfNlDuPwtsOPGchHpIg; fptctx2=taBcrIH61PuCVH7eNCyH0LNKRXFdWqLJ6b8ywJyet7VcjuuBQ1WWQElP4ekrb4u0qRAdAFAyhK2N1bIk9uyuc%252bw0vlV4KveZ9AvdlkH0w2l0ZoH0iHtrIC0iS8QjfEeULEVATpZDgDuW30amp7pNsnHkEF1nB3DyPLQqAgUdg7NHQGNEVP%252bQnwvZQKHW0lpMkexNHgrVKVBjj2xlW4xUDhitBi156CqSkRShlwar85jXldsI5CjPzP9xk30JHKdE0z8tvciS1fp4NFGCcONkl%252bDwMJs7fMX2kQnAi%252bAafsP3BcIHOeCoy%252b99uRfuxfmYp69EsyhQogquyZ5cuwuu3qEP56lt%252bPc%252f1xn9aIogBMA%253d; li_rm=AQGRgZbC_8j1dgAAAY9TRTEdeoiybZAAmOIc6gzUphBB9vSHndOxWiwwxvkhdb5g5cATisGRBKsFaMwqMrIIRcsc9GPFon7ZK875fIG1RMHWuLcCG1zdb0cLzi2SFz4cZdqWhtiDZdWg_OPYGdu51GpY-UQf267sJLT45wfGJkRZx6mjXt0HMk-5Xl8Hn2No1qtOGC5VaTpuhTl92fmpLQuuBYcwUjygOlV6QlyPsaN-rK0lbhq4H864SLSdd-aF-7neOdC3Camode-tcGxtbG0A2wrN8d3Crg3owz40A79slfaxCl6KceKFm6pAL6qlgt7zypEjXo0CV4OP8fg; li_g_recent_logout=v=1&true; visit=v=1&M; li_mc=MTsyMTsxNzE1MDg5MTcxOzI7MDIxNSsjqvzMpEFFk1wue/tCCus4RIsWjr9zJlYYSdid5B8=; lang=v=2&lang=en-us; liap=true; li_at=AQEDAR_M3ngEzBkGAAABj1NO71IAAAGPd1tzUk4AkzX4RtrkW_peVaK4pWKP-1a9SfSAaUeiByAbETz0F7zwuHevzpCJrgcF37j7J4Io_4DlKkpBvOyPGPGB8L2hrHHu55TvTiTWPtYMQXI1TSb2XGMF; JSESSIONID="ajax:0370198051245593824"; lidc="b=TB92:s=T:r=T:a=T:p=T:g=1541:u=212:x=1:i=1715089633:t=1715160766:v=2:sig=AQGbKM8CDDmOk6svvTLwhQbH_UOn6cEP"',
    'dnt': '1',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
}

@dataclass
class searchResult:
    title: str
    subtitle: str
    url: str

@dataclass
class pageData:
    tenure: float

def make_search(search:str, category:int, page:int):
    results = []
    url = f"https://www.linkedin.com/search/results/companies/?industryCompanyVertical=%5B%22{category}%22%5D&keywords={search}&origin=FACETED_SEARCH&page={page}&sid=a9-"
    r = make_request(url=url, headers=headers).text
    soup = BeautifulSoup(r, 'html.parser').find_all()[226].get_text(strip=True)
    data = json.loads(soup)["included"]

    for item in data:
        try:
            results.append(searchResult(title=item["title"]["text"], subtitle=item["primarySubtitle"]["text"], url=item["navigationUrl"]))
        except:
            pass
    
    return results

def temp(term:str, category:int, top_n:int):
    results = []
    counter = 0
    required_pages = ceil(top_n/10)

    for page in range(1, required_pages+1):
        url = f"https://www.linkedin.com/search/results/companies/?industryCompanyVertical=%5B%22{category}%22%5D&keywords={term}&origin=FACETED_SEARCH&page={page}&sid=a9-"
        r = make_request(url=url, headers=headers).text
        soup = BeautifulSoup(r, 'html.parser').find_all()[226].get_text(strip=True)
        data = json.loads(soup)["included"]

        for item in data:
            try:
                if counter < top_n:
                    results.append(searchResult(title=item["title"]["text"], subtitle=item["primarySubtitle"]["text"], url=item["navigationUrl"]))
                    counter += 1
                else:
                    return results
            except:
                pass


def login(driver, username, password):
    driver.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
    driver.implicitly_wait(2)

    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys(username)

    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys(password)

    password_input.send_keys(Keys.RETURN)