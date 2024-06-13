import unittest

from sidt.interfaces.instagram import *


class TestInstagram(unittest.TestCase):

    def test_get_hashtag_popularity(self):
        pop = get_hashtag_popularity("python")

        self.assertTrue(isinstance(pop, int))
        self.assertGreater(pop, 0)
    
    def test_get_profile_info(self):
        info = get_profile_info("nasa")
        print(info)
    


if __name__ == '__main__':
    unittest.main()
