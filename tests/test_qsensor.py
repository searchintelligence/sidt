import json
import unittest

from sidt.interfaces.qsensor import *


class TestQsensor(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestQsensor, self).__init__(*args, **kwargs)
        self.qs = Qsensor()

    def test_get_profile_id(self):
        d = self.qs.get_historical_wait_times("hartsfield-jackson-atlanta-international-airport-tsa-wait-times", 0)
        print(d)
    


if __name__ == '__main__':
    unittest.main()
