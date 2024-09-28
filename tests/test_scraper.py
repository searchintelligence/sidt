import unittest
from sidt.utils.scraper import Scraper

class TestScraper(unittest.TestCase):

    def setUp(self):
        print()
        self.s = Scraper()

    def test_log(self):
        self.s.log("Success Log", level=-1)
        self.s.log("Info Log", level=0)
        self.s.log("Warning Log", level=1)
        self.s.log("Error Log", level=2)

    def test_request(self):
        self.s.request("GET", "https://httpstat.us/200")
        self.s.request("GET", "https://httpstat.us/500")
        self.s.request("GET", "https://httpstat.us/429")
    
    def test_vpn_connect(self):
        self.s.vpn_connect()