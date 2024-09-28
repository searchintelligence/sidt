
import base64
import json
from bs4 import BeautifulSoup
import requests


class Qsensor:
    def __init__(self): None

    def get_historical_wait_times(self, page: str, day: int):
        if day < 0 or day > 6:
            raise Exception("Invalid day, should be from 0 to 6 where Monday is 0")
        
        r = requests.get(
            f"https://qsensor.co/airports/{page}/?ctday={day}"
        ).text

        scripts = BeautifulSoup(r, 'html.parser').find_all('script', {'src': True})
        for script in scripts:
            try:
                base64_data = script['src'].split(',')[1]
                decoded_js = base64.b64decode(base64_data).decode('utf-8')
                if "const dataJson" in decoded_js:
                    data = decoded_js.split("const dataJson = ")[1].split(";\n")[0]
                    return json.loads(data)
            except:
                continue
        return []
