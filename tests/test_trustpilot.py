import unittest

from sidt.interfaces.trustpilot import *


class TestTrustpilot(unittest.TestCase):

    def test_get_site_info(self):
        site_info = get_site_info("trustpilot.com")

        self.assertEqual(site_info["name"], "Trustpilot")
        self.assertEqual(site_info["category"], "Review Site")

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

    # def test_get_reviews(self):
    #     reviews = get_reviews("yeezy.com")
    #     self.assertIsInstance(reviews, list)

    #     self.assertIsInstance(reviews[0], dict)
    #     self.assertIn("title", reviews[0])
    #     self.assertIn("body", reviews[0])
    #     self.assertIn("rating", reviews[0])

    #     self.assertIsInstance(reviews[0]["title"], str)
    #     self.assertIsInstance(reviews[0]["body"], str)
    #     self.assertIsInstance(reviews[0]["rating"], int)


if __name__ == '__main__':
    unittest.main()
