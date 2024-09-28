import json
import unittest

from sidt.interfaces.metacritic import *


class TestMetacritic(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestMetacritic, self).__init__(*args, **kwargs)
        self.meta = Metacritic()

    def test_search(self):
        d = self.meta.search("Elden Ring: Shadow of the Erdtree  ")
        print(json.dumps(d, indent=4))
    
    def test_get_game(self):
        d = self.meta.get_game("otxo")
        print(json.dumps(d, indent=4))


if __name__ == '__main__':
    unittest.main()
