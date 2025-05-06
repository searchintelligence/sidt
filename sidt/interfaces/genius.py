from bs4 import BeautifulSoup
import tls_client


class Genius:

    def __init__(self):
        self.client = tls_client.Session(random_tls_extension_order=True)

    def get_lyrics(self, slug: str):
        r = self.client.get(f"genius.com/{slug}")
        if r.status_code != 200:
            raise Exception(f"Failed to get lyrics for {slug}")

        soup = BeautifulSoup(r.text, "html.parser")
        containers = soup.find_all(attrs={"data-lyrics-container": True})

        return {
            "len": len(containers)
        }

