import time

import tls_client
from tqdm import tqdm


def new_session():
    return tls_client.Session(
        client_identifier="chrome124",
        random_tls_extension_order=True
    )


def make_request(url, method="GET", headers="", cookies="", params=""):
    session = new_session()
    while True:
        response = session.get(url, headers=headers,
                               cookies=cookies, params=params)
        if response.status_code != 200:
            tqdm.write(f"Error {response.status_code} requesting {url}")
            time.sleep(5)
        else:
            return response
