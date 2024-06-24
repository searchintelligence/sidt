import unittest
from sidt.interfaces.tripadvisor import *

# 24166513 - restaurant Orlando Bacan
# 102432 - attraction Universal Studios Florida


class TestTripadvisor(unittest.TestCase):

    def test_us_states(self):
        states = us_states()
        self.assertIsInstance(states, dict)
        self.assertGreater(len(states), 0)
        print(states)
    
    def test_us_cities(self):
        cities = us_cities()
        self.assertIsInstance(cities, dict)
        self.assertGreater(len(cities), 0)
        print(cities)
    
    def test_canada_cities(self):
        cities = canada_cities()
        self.assertIsInstance(cities, dict)
        self.assertGreater(len(cities), 0)
        print(cities)

    def test_search(self):
        results = search("North Myrtle Beach, SC")
        for result in results:
            self.assertIsInstance(result, dict)
            self.assertIsNotNone(result["id"])
            self.assertIsInstance(result["id"], int)
            self.assertIsInstance(result["name"], str)
            self.assertIsInstance(result["long_name"], str)
            self.assertIsInstance(result["latitude"], float)
            self.assertIsInstance(result["longitude"], float)
            self.assertIsInstance(result["type"], str)
            self.assertIn("id", result)
            self.assertIn("name", result)
            self.assertIn("long_name", result)
            self.assertIn("latitude", result)
            self.assertIn("longitude", result)
            self.assertIn("type", result)
            print(result)
            print("\n")

    def test_get_location_types(self):
        types = get_location_types()
        self.assertIsInstance(types, list)
        self.assertGreater(len(types), 0)
        print(types)

    def test_get_review_details(self):
        details_list = [
            get_review_details(102432),
            get_review_details(24166513),
        ]

        for details in details_list:
            self.assertIsInstance(details, dict)
            self.assertIsInstance(details["rating"], (float, int))
            self.assertIsInstance(details["reviews"], int)
            self.assertIsInstance(details["rating_aggregations"], dict)
            self.assertIsInstance(details["language_aggregations"], dict)
            self.assertIn("rating", details)
            self.assertIn("rating_aggregations", details)
            self.assertIn("language_aggregations", details)
            self.assertIn("excelent", details["rating_aggregations"])
            self.assertIn("very_good", details["rating_aggregations"])
            self.assertIn("average", details["rating_aggregations"])
            self.assertIn("poor", details["rating_aggregations"])
            self.assertIn("terrible", details["rating_aggregations"])
            print(details)

    def test_get_filtered_review_count(self):
        count_list = [
            get_filtered_review_count(102432),
            get_filtered_review_count(24166513, "great")
        ]

        for count in count_list:
            self.assertIsInstance(count, int)
            self.assertGreater(count, 0)
            print(count)


if __name__ == '__main__':
    unittest.main()
