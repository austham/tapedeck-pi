import os, time
import RPi.GPIO as GPIO
from dotenv import load_dotenv
from src.spotify_api import SpotifyAuth, SpotifyAPI
from mfrc522 import SimpleMFRC522


load_dotenv()
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

def write_ids_to_tag(reader : SimpleMFRC522):
    while True:
        try:
            text = input("Spotify Album ID to write to tag: ")
            print("Place the tag on the reader. Waiting for tag...")
            reader.write(text)
            print("ID written to tag!")

        except KeyboardInterrupt:
                GPIO.cleanup()
                break

def read_and_play_ids(reader : SimpleMFRC522, spotify : SpotifyAPI):
    while True:
        try:
            print("Waiting for an RFID tag...")
            id, text = reader.read()
            print(f"Tag ID: {id}")
            print(f"Album ID: {text}")
            album = text.strip(" ")
            albuminfo = spotify.get_media(album, "album")
            uri = spotify.id_to_uri(album, "album")
            spotify.play(uri)
            print(f"Now playing {albuminfo['name']} by {albuminfo['artists'][0]['name']}")
            time.sleep(2)

        except KeyboardInterrupt:
            GPIO.cleanup()
            break

if __name__ == '__main__':
    auth = SpotifyAuth(CLIENT_ID, REDIRECT_URI, CLIENT_SECRET)
    spotify = SpotifyAPI(auth.access_token)
    reader = SimpleMFRC522()
    continue_flag = True

    # cli interface
    while continue_flag:
        print("\nWelcome to TapeDeck-Pi! Please select an option:")
        print("1. Write Spotify Album IDs to tags")
        print("2. Play Spotify Albums from tags")
        print("3. Exit")

        option = input("Enter option: ")
        if option == "1":
            write_ids_to_tag(reader)
        elif option == "2":
            read_and_play_ids(reader, spotify)
        elif option == "3":
            print("Exiting...")
            continue_flag = False
        else:
            print("Invalid option!")
