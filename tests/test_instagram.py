import unittest

from sidt.interfaces.instagram import *


class TestInstagram(unittest.TestCase):

    def test_get_profile_id(self):
        id = get_profile_id("brandoncoleman")
        self.assertIsInstance(id, int)
        self.assertGreater(id, 0)
        print(id)

    def test_generate_session_id(self):
        s = generate_session_id()
        self.assertIsInstance(s, str)
        self.assertGreater(len(s), 0)
        print(s)
    
    def test_get_hashtag_populatiry(self):
        pop = get_hashtag_popularity("fyp")
        self.assertIsInstance(pop, int)
        self.assertGreater(pop, 0)
        print(pop)

    def test_make_search_query(self):
        q = make_search_query("nasa")
        print(q)

    def test_user_info(self):
        username = "brandoncoleman"
        i = get_user_info(get_profile_id(username))
        self.assertIsInstance(i, dict)
        self.assertGreater(len(i), 0)
        self.assertDictContainsSubset({"username": username}, i)
        self.assertDictContainsSubset({"id": 12032649}, i)
        self.assertIsInstance(i["followers"], int)
        self.assertIsInstance(i["following"], int)
        self.assertIsInstance(i["posts"], int)
        self.assertGreater(i["followers"], 0)
        self.assertGreater(i["following"], 0)
        self.assertGreater(i["posts"], 0)
        self.assertIsInstance(i["biography"], str)
        print(i)
    
    def test_user_feed(self):
        f = get_user_feed(get_profile_id("rossbutler"))
        self.assertIsInstance(f, list)
        self.assertGreater(len(f), 0)
        print(len(f))
    
    def test_generate_user_analysis(self):
        a = generate_user_analysis("rossbutler")
        print(a)


if __name__ == '__main__':
    unittest.main()
