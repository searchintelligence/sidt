import json
import unittest

from sidt.interfaces.olympics import *


class TestOlympics(unittest.TestCase):

    def test_get_team_usa(self):
        print(len(get_team_usa()))
        print(json.dumps(get_team_usa()[0], indent=2, ensure_ascii=False), "\n")


if __name__ == '__main__':
    unittest.main()
