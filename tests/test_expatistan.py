import unittest

from sidt.interfaces.expatistan import *


class TestTrustpilot(unittest.TestCase):

    def test_search_by_city(self):
        results = search_by_city("lond")

        self.assertEqual(results[0]["id"], "london")
        self.assertEqual(results[0]["name"], "London")
        self.assertEqual(results[0]["country"], "gb")
    
    def test_get_countries(self):
        countries = get_countries()

        self.assertIsInstance(countries, dict)
        self.assertGreater(len(countries), 0)
        self.assertEqual(countries["japan"], "JP")
        self.assertEqual(countries["finland"], "FI")

    def test_get_cost_of_living_city(self):
        items = get_cost_of_living("london", "USD")

        self.assertIsInstance(items, dict)
        self.assertGreater(len(items), 0)
        self.assertIn("12 eggs, large", items)
        self.assertIn("Monthly ticket public transport", items)
        self.assertIn("Tube of toothpaste", items)
        self.assertIn("2 tickets to the movies", items)
    
    def test_get_cost_of_living_country(self):
        items = get_cost_of_living("United Kingdom", "GBP")

        self.assertIsInstance(items, dict)
        self.assertGreater(len(items), 0)
        self.assertIn("12 eggs, large", items)
        self.assertIn("Monthly ticket public transport", items)
        self.assertIn("Tube of toothpaste", items)
        self.assertIn("2 tickets to the movies", items)


if __name__ == '__main__':
    unittest.main()
