import os, time
import RPi.GPIO as GPIO
from dotenv import load_dotenv
from src.spotify_api import SpotifyAuth, SpotifyAPI
from mfrc522 import SimpleMFRC522


load_dotenv()
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

if __name__ == '__main__':
    auth = SpotifyAuth(CLIENT_ID, REDIRECT_URI, CLIENT_SECRET)
    spotify = SpotifyAPI(auth.access_token)
    reader = SimpleMFRC522()
    try:
        while True:
            id, text = reader.read()
            print(id)
            print(text)
            album = text.strip(" ")
            albuminfo = spotify.get_media(album, "album")
            print(albuminfo["name"])
            print(albuminfo["artists"][0]["name"])
            uri = spotify.id_to_uri(album, "album")
            spotify.play(uri)
            time.sleep(10)


    except KeyboardInterrupt:
        GPIO.cleanup()