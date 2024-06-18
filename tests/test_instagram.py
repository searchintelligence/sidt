import unittest

from sidt.interfaces.instagram import *


class TestInstagram(unittest.TestCase):

    def test_get_hashtag_popularity(self):
        pop = get_hashtag_popularity("python")

        self.assertIsInstance(pop, int)
        self.assertGreater(pop, 0)
        print(pop)

    def test_get_profile_info(self):
        info = get_profile_info("nasa")
        self.assertIn("follower_count", info)
        self.assertIn("following_count", info)
        self.assertIsInstance(info["follower_count"], int)
        self.assertIsInstance(info["following_count"], int)
        self.assertGreater(info["follower_count"], 0)
        self.assertGreater(info["following_count"], 0)
        print(info)
    
    def test_get_inzpire_data(self):
        data = get_inzpire_data("drake.maye", currency="USD", posts=1, stories=1)
        print(data)
    
    def test_get_picuki_data(self):
        data = get_picuki_data("dariusmuasau")
        print(data)


if __name__ == '__main__':
    unittest.main()
