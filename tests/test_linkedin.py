import json
import unittest

from sidt.interfaces.linkedin import *


class TestLinkedin(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestLinkedin, self).__init__(*args, **kwargs)
        self.l = Linkedin()

    def test_search(self):
        d = self.l.search("Python Developer", "Toronto")
        print(json.dumps(d[:5], indent=4))
        print(len(d))
        # print(d)
        # print(len(d))
        # for i in d:
        #     print(i)
    
    def test_get_job_count(self):
        print(self.l.get_job_count("Game Developer", "Los Angeles, CA"))
        
        
    


if __name__ == '__main__':
    unittest.main()
