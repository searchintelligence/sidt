import unittest

from sidt.interfaces.trustpilot import *


class TestTrustpilot(unittest.TestCase):

    def setUp(self):
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            # 'cookie': 'TP.uuid=3752ac4e-7a0c-45ef-9805-845abfc397d5; OptanonAlertBoxClosed=2024-03-30T19:49:59.728Z; OptanonConsent=isGpcEnabled=0&datestamp=Fri+May+03+2024+20%3A04%3A15+GMT%2B0100+(British+Summer+Time)&version=6.28.0&isIABGlobal=false&hosts=&consentId=83967eae-b7be-46e3-b505-2dbf8058d0ca&interactionCount=2&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A0%2CC0003%3A0%2CC0004%3A0&geolocation=GB%3BENG&AwaitingReconsent=false',
            'dnt': '1',
            'priority': 'u=0, i',
            'referer': 'https://www.trustpilot.com/',
            'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        }

    def test_getSiteInfo(self):
        site_info = get_site_info("trustpilot.com", self.headers)

        self.assertIsInstance(site_info, Trustpilot)
        self.assertEqual(site_info.name, "Trustpilot")
        self.assertEqual(site_info.category, "Review Site")

    def test_make_search(self):
        results = make_search("trustpilot", 10, "US")
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 10)

        self.assertEqual(results[0]["id"], "trustpilot.com")
        self.assertEqual(results[0]["name"], "Trustpilot")

        self.assertIsInstance(results[0]["numberOfReviews"], int)
        self.assertGreater(results[0]["numberOfReviews"], 0)

        self.assertIsInstance(results[0]["stars"], int)
        self.assertIsInstance(results[0]["trustScore"], float)


if __name__ == '__main__':
    unittest.main()
