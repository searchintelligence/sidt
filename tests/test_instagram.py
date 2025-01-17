import unittest

from sidt.interfaces.instagram import *


class TestInstagram(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestInstagram, self).__init__(*args, **kwargs)
        self.insta = Instagram("64879496178%3AEbd7XfUecybXa3%3A17%3AAYfaTaDENGLHA5EsmUv0kMU_MY399qG-lCuW5AY6bQ")

    def test_get_profile_id(self):
        id = self.insta.get_profile_id("brandoncoleman")
        self.assertIsInstance(id, int)
        self.assertGreater(id, 0)
        print(id)
    
    def test_get_hashtag_populatiry(self):
        pop = self.insta.get_hashtag_popularity("fyp")
        self.assertIsInstance(pop, int)
        self.assertGreater(pop, 0)
        print(pop)

    def test_make_search_query(self):
        q = self.insta.make_search_query("nasa")
        print(q)

    def test_user_info(self):
        username = "brandoncoleman"
        i = self.insta.get_user_info(self.insta.get_profile_id(username))
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
        f = self.insta.get_user_feed(self.insta.get_profile_id("rossbutler"))
        self.assertIsInstance(f, list)
        self.assertGreater(len(f), 0)
        print(len(f))
    
    def test_generate_user_analysis(self):
        a = self.insta.generate_user_analysis("rossbutler")
        print(a)


if __name__ == '__main__':
    unittest.main()
