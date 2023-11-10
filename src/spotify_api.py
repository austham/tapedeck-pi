import requests, os, webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlencode
from dotenv import load_dotenv
load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
AUTH_CODE = ""

REDIRECT_HOST = REDIRECT_URI.split(":")[1].replace("//", "")
REDIRECT_PORT = int(REDIRECT_URI.split(":")[2].split("/")[0])

class SpotifyAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.server.code = self.path.split("=")[1]
        self.wfile.write(b"Success! You may now close this window.")


class SpotifyAuth:
    def get_auth_url(self, client_id, redirect_uri, scope):
        # reponse_type is always "code"
        params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "scope": scope,
            "response_type": "code"
        }
        auth_url = f"https://accounts.spotify.com/authorize?"
        response = requests.get(auth_url + urlencode(params))
        return response.url
        
    def get_auth_code(self, auth_url):
        webbrowser.open(auth_url)
        with HTTPServer((REDIRECT_HOST, REDIRECT_PORT), SpotifyAuthHandler) as server:
            server.handle_request()
            return server.code

class SpotifyAPI:

    #TODO refactor to use new auth flow

    def __init__(self, client_id, client_secret):
        self.auth_token = self.get_auth_token(client_id, client_secret)
        self.auth_header = {"Authorization" : f"Bearer {self.auth_token}"}
        self.base_url = "https://api.spotify.com/v1"


    def get_auth_token(self, client_id, client_secret):

        response = requests.post("https://accounts.spotify.com/api/token",
            headers = {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            data = {
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret
            }
        )
        if response.status_code != 200:
            raise KeyError(f"Could not get Spotify auth token. Check your client ID and client secret. \n Response: {response.json()}")

        return response.json()["access_token"]


    def get_album(self, id):

        response = requests.get(f"{self.base_url}/albums/{id}",
            headers = self.auth_header
        )
        if response.status_code != 200:
            raise KeyError(f"Could not get album. Check your album ID. \n Response: {response.json()}")

        return response.json()
    

    def play(self, uri):
        response = requests.put(f"{self.base_url}/me/player/play",
            headers = self.auth_header,
            json = {
                "context_uri": uri
            }
        )
        if response.status_code != 200:
            raise KeyError(f"Could not play. Check your URI. \n Response: {response.json()}")

        return response.json()
    

    def id_to_uri(self, id, type):

        if type in ["album", "artist", "playlist", "track"]:
            return f"spotify:{type}:{id}"
        
        raise ValueError(f"Type must be of album, artist, playlist, or track. Received {type}")


if __name__ == "__main__":
    spotifyauth = SpotifyAuth()
    auth_url = spotifyauth.get_auth_url(CLIENT_ID, REDIRECT_URI, "user-read-playback-state")
    AUTH_CODE = spotifyauth.get_auth_code(auth_url)
    print(AUTH_CODE)    