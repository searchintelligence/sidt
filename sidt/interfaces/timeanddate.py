from datetime import datetime, timedelta
import json
from bs4 import BeautifulSoup
import requests


class Timeanddate:
    def __init__(self):
        pass

    def get_locations(self):
        response = requests.get("https://www.timeanddate.com/weather/uk")
        soup = BeautifulSoup(response.text, "html.parser").find(class_="zebra")
        locations = []
        for a in soup.find_all("a", href=True):
            if "/weather/" in a["href"]:
                locations.append(a["href"].split("/weather/")[1])
        return locations

    def get_weather_history(self, location: str, start_date: datetime, end_date: datetime = datetime.now()):
            history = {}
            current_date = start_date

            start_timestamp = start_date.timestamp() * 1000
            end_timestamp = (end_date + timedelta(days=1)).timestamp() * 1000

            while current_date <= end_date:
                response = requests.get(
                    f"https://www.timeanddate.com/weather/{location}/historic",
                    params={
                        "month": current_date.month,
                        "year": current_date.year,
                    },
                )
                soup = BeautifulSoup(response.text, "html.parser")
                script = soup.find('script', text=lambda t: t and 'var data=' in t)
                
                if script:
                    data = json.loads(script.string.split('var data=')[1].split(';')[0].strip())
                    for record in data["detail"]:
                        record_date = datetime.fromtimestamp(record["date"] / 1000).strftime('%Y-%m-%d')
                        if start_timestamp <= record["date"] < end_timestamp:
                            if record_date not in history:
                                history[record_date] = []
                            history[record_date].append(record)
                
                if current_date.month == 12:
                    current_date = current_date.replace(year=current_date.year + 1, month=1)
                else:
                    current_date = current_date.replace(month=current_date.month + 1)

            return history
