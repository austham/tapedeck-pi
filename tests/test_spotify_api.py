import unittest
from unittest.mock import patch
from requests import Session
from src.spotify_api import SpotifyAPI


class TestSpotifyAPI_Positive(unittest.TestCase):
    def setUp(self):
        self.access_token = 'test_access_token'
        self.spotify = SpotifyAPI(self.access_token)

    @patch.object(Session, 'get')
    def test_get_media(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"test": "test"}
        result = self.spotify.get_media('id', 'album')
        self.assertEqual(result, {"test": "test"})

    @patch.object(Session, 'get')
    def test_get_media_none(self, mock_get):
        mock_get.return_value.status_code = 404
        result = self.spotify.get_media('id', 'album')
        self.assertEqual(result, None)

    @patch.object(Session, 'put')
    def test_play(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"test": "test"}
        result = self.spotify.play('id')
        self.assertEqual(result, {"test": "test"})

    def test_id_to_uri(self):
        self.assertEqual(self.spotify.id_to_uri('id', "track"), "spotify:track:id")

    def test_type_is_media(self):
        self.assertTrue(self.spotify.type_is_media("album"))
        self.assertTrue(self.spotify.type_is_media("artist"))
        self.assertTrue(self.spotify.type_is_media("playlist"))
        self.assertTrue(self.spotify.type_is_media("track"))

class TestSpotifyAPI_Negative(unittest.TestCase):
    def setUp(self):
        self.access_token = 'test_access_token'
        self.spotify = SpotifyAPI(self.access_token)

    def test_get_media_bad_type(self):
        with self.assertRaises(ValueError):
            self.spotify.get_media('id', 'bad_type')

    def test_id_to_uri_bad_type(self):
        with self.assertRaises(ValueError):
             self.spotify.id_to_uri('0q9e8xVGwYZiYl9O08f2Ox', "bad_type")

    def test_type_is_media_bad_type(self):
        self.assertFalse(self.spotify.type_is_media("bad_type"))

    @patch.object(Session, 'get')
    def test_get_media_bad_response(self, mock_get):
        mock_get.return_value.status_code = 400
        with self.assertRaises(KeyError):
            self.spotify.get_media('id', 'album')

    @patch.object(Session, 'put')
    def test_play_bad_response(self, mock_get):
        mock_get.return_value.status_code = 400
        with self.assertRaises(KeyError):
            self.spotify.play('id')


if __name__ == '__main__':
    unittest.main()