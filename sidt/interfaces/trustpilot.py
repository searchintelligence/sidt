import re
from ..utils.api import make_request
from bs4 import BeautifulSoup
from tqdm import tqdm


def get_release_number():
    """
    Retrieves the current release number from the Trustpilot website.

    Returns:
        str: The current release number if found, None otherwise.
    """
    r = make_request("https://www.trustpilot.com/review/www.tripadvisor.com", method="GET").text
    pattern = re.compile(r'"currentReleaseNumber":"businessunitprofile-consumersite@\d+\.\d+\.\d+')
    match = pattern.search(r)
    if match:
        return match.group(0).split('@')[1]
    else:
        raise Exception("Failed to get release number")

def process_reviews(response):
    """
    Process the reviews from the response and return a list of dictionaries containing the title, body, and rating.

    Args:
        response (dict): The response containing the reviews.

    Returns:
        list: A list of dictionaries, where each dictionary represents a review and contains the following keys:
            - "title" (str): The title of the review.
            - "body" (str): The body of the review.
            - "rating" (int): The rating of the review.
    """
    reviews = []
    for review in response["pageProps"]["reviews"]:
        reviews.append({
            "title": review["title"],
            "body": review["text"],
            "rating": review["rating"]
        })
    return reviews


def get_reviews(id):
    """
    Retrieves reviews for a given Trustpilot business unit ID.

    Args:
        id (str): The Trustpilot business unit ID.

    Returns:
        list: A list of reviews for the specified business unit ID.
    """
    reviews = []
    headers = {'x-nextjs-data': '1'}
    url = f"https://www.trustpilot.com/_next/data/businessunitprofile-consumersite-{get_release_number()}/review/{id}.json?businessUnit={id}"

    r = make_request(url=url, method="GET", headers=headers).json()
    reviews.extend(process_reviews(r))

    pages = r["pageProps"]["filters"]["pagination"]["totalPages"]
    if pages > 1:
        for p in tqdm(range(2, pages+1), leave=False):
            r = make_request(url=f"{url}&page={p}", method="GET", headers=headers).json()
            reviews.extend(process_reviews(r))

    return reviews


def get_site_info(id: str):
    """
    Retrieves information about a site from Trustpilot.

    Args:
        id (str): The ID of the site.

    Returns:
        dict: A dictionary containing the following information:
            - id (str): The ID of the site.
            - name (str): The name of the site.
            - review_count (int): The number of reviews for the site.
            - rating_class (str): The rating class of the site.
            - score (str): The score of the site.
            - category (str): The category of the site, if available.
    """
    url = f"https://www.trustpilot.com/review/{id}"
    r = make_request(url=url, method="GET").text

    soup = BeautifulSoup(r, 'html.parser').find(
        attrs={"id": "business-unit-title"})

    name = soup.find("h1").find_all("span")[0].get_text(strip=True)
    review_count = int(soup.find("span", role="link").get_text().split("•")[
                       0].strip().replace(",", ""))
    rating_class = soup.find(
        "span", role="link").get_text().split("•")[-1].strip()
    score = soup.find(
        "div", {"data-rating-component": "true"}).find("p").get_text(strip=True)

    category_link = soup.find("a", href=lambda x: x and "/categories/" in x)
    category = category_link.get_text(strip=True) if category_link else None

    return {
        "id": id,
        "name": name,
        "review_count": review_count,
        "rating_class": rating_class,
        "score": score,
        "category": category
    }


def make_search(query: str, result_size: int = 100, country: str = "US"):
    """
    Performs a search on Trustpilot for business units based on the given query.

    Args:
        query (str): The search query.
        result_size (int, optional): The maximum number of results to return. Defaults to 100.
        country (str, optional): The country to search in. Defaults to "US".

    Raises:
        ValueError: If result_size is greater than 100.

    Returns:
        list: A list of dictionaries containing information about the business units found in the search.
            Each dictionary contains the following keys:
            - id: The identifying name of the business unit.
            - name: The display name of the business unit.
            - numberOfReviews: The number of reviews for the business unit.
            - trustScore: The trust score of the business unit.
            - stars: The star rating of the business unit.
            - websiteUrl: The website URL of the business unit.
            - verified: Whether the business unit is verified or not.
    """

    if result_size > 100:
        raise ValueError("result_size must be less than or equal to 100")

    results = []

    url = f"https://www.trustpilot.com/api/consumersitesearch-api/businessunits/search?country={country}&pageSize={result_size}&query={query}"
    r = make_request(url=url, method="GET").json()

    for item in r["businessUnits"]:
        results.append({
            "id": item["identifyingName"],
            "name": item["displayName"],
            "numberOfReviews": item["numberOfReviews"],
            "trustScore": item["score"]["trustScore"],
            "stars": item["score"]["stars"],
            "websiteUrl": item["websiteUrl"],
            "verified": item["verified"],
        })

    return results
