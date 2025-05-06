import json
import unittest

from sidt.interfaces.glassdoor import *


class TestGlassdoor(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestGlassdoor, self).__init__(*args, **kwargs)
        self.gd = Glassdoor()

    def test_search(self):
        d = self.gd.search("machine learning", 2280, "STATE")
        # print(json.dumps(d[:5], indent=4))
        # print(len(d))
        for i in d:
            print(i)
        
    def test_get_location(self):
        d = self.gd.get_location("New York")
        print(d)
        
    


if __name__ == '__main__':
    unittest.main()
