import time

import tls_client
from tqdm import tqdm


def new_session():
    return tls_client.Session(
        client_identifier="chrome124",
        random_tls_extension_order=True
    )


def make_request(url:str, method:str="GET", persistant:bool=True, headers:dict=None, cookies:dict=None, params:dict=None, json:dict=None):
    session = new_session()
    while True:
        response = session.execute_request(url=url, method=method, headers=headers,
                               cookies=cookies, params=params, json=json, allow_redirects=True)
        if response.status_code != 200 and persistant:
            tqdm.write(f"Error {response.status_code} requesting {url}")
            time.sleep(5)
        else:
            return response
