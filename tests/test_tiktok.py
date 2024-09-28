import json
import unittest

from sidt.interfaces.tiktok import *


class TestTiktok(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestTiktok, self).__init__(*args, **kwargs)
        self.tiktok = Tiktok()

    def test_hashtag(self):
        d = self.tiktok.get_hashtag_info("docmartens")
        print(json.dumps(d, indent=4))
    
    def test_search(self):
        d = self.tiktok.search("google", "user")
        print(json.dumps(d, indent=4))
        # print(d)
    
    def test_get_user(self):
        d = self.tiktok.get_user("nike")
        print(d)


if __name__ == '__main__':
    unittest.main()
