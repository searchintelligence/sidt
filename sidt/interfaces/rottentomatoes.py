from bs4 import BeautifulSoup
from sidt.utils.api import make_request


def make_search(term:str):
    results = {}

    url = "https://www.rottentomatoes.com/search?search=the%20batma"
    r = make_request(url=url, method="GET").text
    soup = BeautifulSoup(r, "html.parser")

    result_groups = soup.find_all("search-page-result")
    for group in result_groups:
        category = group.find(attrs={"slot": "title"}).get_text(strip=True)
        results[category] = []
        items = group.find_all("search-page-media-row")
        print(len(items))
        for item in items:
            try: title = item.find(class_="title").get_text(strip=True)
            except: title = None
            try: year = item.find(class_="year").get_text(strip=True)
            except: year = None
            try: cast = item.find(class_="cast").get_text(strip=True)
            except: cast = None
            results[category].append({"title": title, "year": year, "cast": cast})
    return results