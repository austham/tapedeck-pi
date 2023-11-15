from src.spotify_api import SpotifyAuth, SpotifyAPI

from dotenv import load_dotenv
import os

load_dotenv()
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

if __name__ == '__main__':
    auth = SpotifyAuth(CLIENT_ID, REDIRECT_URI, CLIENT_SECRET)
    spotify = SpotifyAPI(auth.access_token)
    spotify.play('0q9e8xVGwYZiYl9O08f2Ox', 'album')