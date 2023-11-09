import unittest
import os

from src.spotify_api import SpotifyAPI
from dotenv import load_dotenv
load_dotenv()

CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')


class TestSpotifyAPI(unittest.TestCase):
    def setUp(self):
        self.spotify_api = SpotifyAPI(CLIENT_ID, CLIENT_SECRET)

    def test_get_auth_token(self):
        self.assertTrue(self.spotify_api.auth_token)

    def test_get_album(self):
        self.assertIsNotNone(self.spotify_api.get_album('0q9e8xVGwYZiYl9O08f2Ox?si=Lr4hwg7iSk6ExpD2FDnnJw'))

    def test_play(self):
        self.spotify_api.play('spotify:album:0q9e8xVGwYZiYl9O08f2Ox?si=Lr4hwg7iSk6ExpD2FDnnJw')


class NegativeTestSpotifyAPI(unittest.TestCase):
    def setUp(self):
        self.spotify_api = SpotifyAPI(CLIENT_ID, CLIENT_SECRET)

    def test_get_auth_token_keyerror(self):
        self.assertRaises(KeyError, SpotifyAPI, 'dummy', 'dummy')

    def test_get_album_invalid_id(self):
        self.assertRaises(KeyError, self.spotify_api.get_album, 'foobar123')

    def test_play(self):
        pass



if __name__ == '__main__':
    unittest.main()