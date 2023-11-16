import os
from dotenv import load_dotenv
from src.spotify_api import SpotifyAuth, SpotifyAPI


load_dotenv()
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

if __name__ == '__main__':
    auth = SpotifyAuth(CLIENT_ID, REDIRECT_URI, CLIENT_SECRET)
    spotify = SpotifyAPI(auth.access_token)