from bs4 import BeautifulSoup
from ..utils.api import make_request
from dataclasses import dataclass

@dataclass
class searchResult:
    id: str
    title: str
    subtitle: str
    rank: int
    year: int
    category: str

def make_search(term:str, type:str=None) -> list[searchResult]:
    """
    Perform a search on IMDb based on the given term and type.

    Args:
        term (str): The search term.
        type (str, optional): The type of search. Can be "titles" or "names". Defaults to None.

    Returns:
        list[searchResult]: A list of search results.

    Raises:
        ValueError: If the type is provided but not one of the accepted types.

    """
    results = []

    accepted_types = ["titles", "names"]
    if type:
        if type not in accepted_types:
            raise ValueError(f"Type must be one of {accepted_types}, not {type}.")
        url = f"https://v3.sg.media-imdb.com/suggestion/{type}/x/{term}.json"
    else:
        url = f"https://v3.sg.media-imdb.com/suggestion/x/{term}.json"
    
    r = make_request(url=url, method="GET").json()["d"]
    for item in r:
        try: id = item["id"]
        except: id = None
        try: title = item["l"]
        except: title = None
        try: subtitle = item["s"]
        except: subtitle = None
        try: rank = item["rank"]
        except: rank = None
        try: year = item["y"]
        except: year = None
        try: category = item["qid"]
        except: category = None
        results.append(searchResult(id, title, subtitle, rank, year, category))
    
    return results

def get_actor_filmography(actor_id: str) -> dict:
    """
    Retrieves the filmography of an actor from IMDb.

    Args:
        actor_id (str): The IMDb ID of the actor.

    Returns:
        dict: A dictionary containing the filmography of the actor, organized by table name.
              The keys are the table names and the values are lists of film IDs.
    """
    filmography = {}

    url = f"https://pro.imdb.com/name/{actor_id}"
    r = make_request(url=url, method="GET").text

    credits = BeautifulSoup(r, 'html.parser').find(attrs={"data-a-name": "credits"})
    sections = credits.find_all(class_="a-section")[1:]

    for section in sections:
        try: 
            table_name = section.find("table").get("id")
            if table_name not in filmography:
                filmography[table_name] = []
        except:
            continue

        items = section.find_all(class_="filmography_row")
        for item in items:
            film_id = item.get('data-filter-item-id')
            filmography[table_name].append(film_id)
            
    return filmography

def get_film_info(film_id: str) -> dict:
    """
    Retrieves information about a film from IMDb based on the film ID.

    Args:
        film_id (str): The IMDb ID of the film.

    Returns:
        dict: A dictionary containing the following film information:
            - title (str): The title of the film.
            - year (str): The release year of the film.
            - age_rating (str): The age rating of the film.
            - run_time (str): The duration of the film.
            - rating (str): The IMDb rating of the film.
            - review_count (str): The number of reviews for the film.
    """
    url = f"https://www.imdb.com/title/{film_id}/"
    r = make_request(url=url, method="GET").text

    soup = BeautifulSoup(r, 'html.parser')
    try: title = soup.find(attrs={"data-testid": "hero__primary-text"}).get_text(strip=True)
    except: title = None
    sublist = soup.find(class_="ipc-inline-list ipc-inline-list--show-dividers sc-d8941411-2 cdJsTz baseAlt")
    try: year = sublist.find_all("li")[0].get_text(strip=True)
    except: year = None
    try: age_rating = sublist.find_all("li")[1].get_text(strip=True)
    except: age_rating = None
    try: run_time = sublist.find_all("li")[2].get_text(strip=True)
    except: run_time = None
    try: rating = soup.find(attrs={"data-testid": "hero-rating-bar__aggregate-rating__score"}).get_text(strip=True).replace("/10", "")
    except: rating = None
    try: review_count = soup.find(class_="sc-bde20123-3 gPVQxL").get_text(strip=True)
    except: review_count = None

    return {
        "title": title,
        "year": year,
        "age_rating": age_rating,
        "run_time": run_time,
        "rating": rating,
        "review_count": review_count
    }