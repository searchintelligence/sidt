import unittest

from sidt.interfaces.google import *

# Legends 169 0x4876a694b594a041:0x2c332c14a80bfbe2
# Luton 18k+ 0x487637d0e4f706d5:0x2e06e7f34ad91ad0
# JAN airport 1233 0x86282b80878caac7:0xce9be786f0b57b5b

class TestGoogle(unittest.TestCase):

    def test_get_id(self):
        id = get_id("luton airport")
        print(id)

    def test_get_review_overview(self):
        results = get_review_overview("0x47d9a1d2b65d9273:0x30038ae01e146e79")
        print(results)

    def test_get_reviews(self):
        results = get_reviews("0x86282b80878caac7:0xce9be786f0b57b5b")
        for result in results["reviews"]:
            print(result)
        print(results["max_reached"])
        print(results["reviews_found"])
        print(results["pages"])
    
    def test_temp(self):
        results = temp("0x487637d0e4f706d5:0x2e06e7f34ad91ad0")
        print(results)
    

if __name__ == '__main__':
    unittest.main()
