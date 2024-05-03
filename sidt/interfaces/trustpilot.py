from ..utils.api import makeRequest
from dataclasses import dataclass
from bs4 import BeautifulSoup
from tqdm import tqdm


@dataclass
class Review:
    heading: str
    body: str
    rating: int
    keywords: list[str]


@dataclass
class Trustpilot:
    id: str
    name: str
    review_count: int
    rating_class: str
    score: float
    category: str


def processReviews(response) -> list[Review]:
    reviews = []
    for review in response["pageProps"]["reviews"]:
        heading = review["title"]
        body = review["text"]
        rating = review["rating"]
        reviews.append(Review(heading, body, rating))
    return reviews


def getReviews(id, headers) -> list[Review]:
    reviews = []
    url = f"https://www.trustpilot.com/_next/data/businessunitprofile-consumersite-2.388.0/review/{id}.json?businessUnit={id}"
    r = makeRequest(url=url, method="GET", headers=headers).json()
    reviews.append(processReviews(r))

    pages = r["pageProps"]["filters"]["pagination"]["totalPages"]
    if pages > 1:
        for p in tqdm(range(2, pages), leave=False):
            url += f"&?page={p}"
            r = makeRequest(url=url, method="GET", headers=headers).json()
            reviews.append(processReviews(r))
    
    return reviews


def getSiteInfo(id, headers) -> Trustpilot:
    url = f"https://www.trustpilot.com/review/{id}"
    r = makeRequest(url=url, method="GET", headers=headers).text

    soup = BeautifulSoup(r, 'html.parser').find(attrs={"id": "business-unit-title"})

    name = soup.find("h1").find_all("span")[0].get_text(strip=True)
    review_count = int(soup.find("span", role="link").get_text().split("•")[0].strip().replace(",", ""))
    rating_class = soup.find("span", role="link").get_text().split("•")[-1].strip()
    score = soup.find("div", {"data-rating-component": "true"}).find("p").get_text(strip=True)

    category_link = soup.find("a", href=lambda x: x and "/categories/" in x)
    category = category_link.get_text(strip=True) if category_link else None

    return Trustpilot(id, name, review_count, rating_class, score, category)