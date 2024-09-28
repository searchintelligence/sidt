import unittest

from sidt.interfaces.spotify import *


class TestSpotify(unittest.TestCase):

    def test_generate_bearer_token(self):
        print(generate_bearer_token())

    def test_get_token(self):
        auth = Auth("24fda6b3d6f84f21a67a78eacdb180b3", "4f34d3d0ddb443a4bad6810c745544ec")
        print(get_token(auth))
    
    def test_get_album(self):
        li = [
            "spotify:album:6RfgcwsOUlWkGNAd6zjjYd",
        ]
        for i in li:
            print(get_album(i))

    def test_get_track(self):
        auth = generate_bearer_token()
        li = [
            "spotify:track:62AuGbAkt8Ox2IrFFb8GKV",
            "spotify:track:0Ai6qtPfiEYGCqBGJYWD1W",
            "spotify:track:0b7j16ybxD7YJFtj8dou8Z",
        ]
        for i in li:
            print(get_track(i, auth))


if __name__ == '__main__':
    unittest.main()
