import time
from bs4 import BeautifulSoup
import requests


class Linkedin:
    def __init__(self):
        pass

    def get_job_count(self, query: str, location: str):
        try_count = 0
        for _ in range(10):
            try:
                response = requests.get(
                    "https://www.linkedin.com/jobs/search",
                    params = {
                        'distance': 0,
                        'keywords': query,
                        'location': location,
                        'geoId': '',
                    },
                )
                expected_result_count = BeautifulSoup(response.text, "html.parser").find(class_="results-context-header__job-count").get_text()
                return expected_result_count
            except: time.sleep(2)

    def search(self, query: str, location: str):
        results = []
        try_count = 0

        for _ in range(10):
            try:
                response = requests.get(
                    "https://www.linkedin.com/jobs/search",
                    params = {
                        'distance': 0,
                        'keywords': query,
                        'location': location,
                        'geoId': '',
                    },
                )
                expected_result_count = BeautifulSoup(response.text, "html.parser").find(class_="results-context-header__job-count").get_text()
            except: time.sleep(2)
            else: break

        while True:
            response = requests.get(
                "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search",
                params={
                    "keywords": query,
                    "location": location,
                    "geoId": "",
                    "start": len(results),
                },
            )
            items = BeautifulSoup(response.text, "html.parser").find_all(
                class_="base-card")
            if items:

                try_count = 0

                for item in items:
                    try:
                        list_date = item.find(
                            class_="job-search-card__listdate").get("datetime")
                    except:
                        try:
                            list_date = item.find(
                                class_="job-search-card__listdate--new").get("datetime")
                        except:
                            list_date = None
                    results.append({
                        "title": item.find(class_="base-search-card__title").get_text().strip(),
                        "employer": item.find(class_="base-search-card__subtitle").get_text().strip(),
                        "location": item.find(class_="job-search-card__location").get_text().strip(),
                        "list_date": list_date,
                    })

            elif try_count >= 10:
                return {
                    "expected_result_count": expected_result_count,
                    "actual_result_count": len(results),
                    "results": results,
                }
            else:
                try_count += 1
                time.sleep(2)





        