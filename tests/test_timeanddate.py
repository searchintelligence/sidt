from datetime import datetime
import json
import unittest

from sidt.interfaces.timeanddate import *


class TestTimeanddate(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestTimeanddate, self).__init__(*args, **kwargs)
        self.t = Timeanddate()

    def test_get_weather_history(self):
        d = self.t.get_weather_history("uk/aberdeen", datetime(2024, 6, 25), datetime(2024, 6, 30))
        # print(len(d))
        print(json.dumps(d, indent=4))
    
    def test_get_locations(self):
        d = self.t.get_locations()
        print(d)



if __name__ == '__main__':
    unittest.main()
