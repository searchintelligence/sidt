from datetime import datetime
import json
import unittest

from sidt.interfaces.steam import *


class TestSteam(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestSteam, self).__init__(*args, **kwargs)
        self.steam = Steam()
    
    def test_search_store(self):
        d = self.steam.search_store("Rocket League")
        for i in d:
            print(json.dumps(i, indent=2, ensure_ascii=False), "\n")

    def test_get_reviews(self):
        max = 30
        d = self.steam.get_reviews(730, max=max)
        for i in d:
            print(json.dumps(i, indent=2, ensure_ascii=False), "\n")
        self.assertEqual(len(d), max)



if __name__ == '__main__':
    unittest.main()
