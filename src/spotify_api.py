import requests, webbrowser, base64
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlencode

class SpotifyAPI:
    # class to handle requests to the Spotify API
    # docs: https://developer.spotify.com/documentation/web-api/reference/
    def __init__(self, access_token) -> None:
        # access_token is retrieved from SpotifyAuth class
        self.base_url = "https://api.spotify.com/v1"
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {access_token}"})

    def play(self, uri) -> dict:
        #TODO: Add support for no active device, play playlist, play artist
        response = self.session.put(f"{self.base_url}/me/player/play",
            json = {
                "context_uri": uri,
            }
        )
        if response.status_code != 200:
            raise KeyError(f"Could not play {uri}! \n Response: {response.json()}")

        return response.json()
    
    def get_media(self, id, type) -> dict:
        if not self.type_is_media(type):
            raise ValueError(f"Type must be of album, artist, playlist, or track. Received {type}")
        
        response = self.session.get(f"{self.base_url}/{type}s/{id}")
        if response.status_code == 404:
            return None
        if response.status_code != 200:
            raise KeyError(f"Could not get {type}! \n Response: {response.json()}")
        return response.json()
    
    def id_to_uri(self, id, type) -> str:
        if not self.type_is_media(type):
            raise ValueError(f"Type must be of album, artist, playlist, or track. Received {type}")
        return f"spotify:{type}:{id}"
    
    def type_is_media(self, type) -> bool:
        if type in ["album", "artist", "playlist", "track"]:
            return True
        return False


# SpotifyAuth class and SpotifyAuthHandler class are used to handle the authorization code flow     
# for the Spotify API. The SpotifyAuth class is used to retrieve the access token and refresh token 
# from Spotify. The SpotifyAuthHandler class is used to handle the request sent to the redirect URI 
# by Spotify during the authorization code flow, capture and store the auth code.                   
# Docs: https://developer.spotify.com/documentation/web-api/tutorials/code-flow                     

class SpotifyAuth:
    # Client ID, Client Secret, and Redirect URI can be found in the app 
    # settings from https://developer.spotify.com/dashboard
    def __init__(self, client_id, redirect_uri, client_secret) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        auth_code = self.request_auth_code(self.request_auth_url())
        tokens = self.request_access_token(auth_code)
        self.access_token = tokens["access_token"]
        self.refresh_token = tokens["refresh_token"]

    def request_auth_url(self) -> str:
        # submit Client ID and Redirect URI to Spotify 
        # reponse_type is always "code"
        # only user-modify-playback-state scope needed for this application
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": "user-modify-playback-state",
            "response_type": "code"
            }
        target_url = f"https://accounts.spotify.com/authorize?"
        response = requests.get(target_url + urlencode(params))
        return response.url

    def request_auth_code(self, auth_url) -> str:
        # opening the auth_url in a browser will redirect to the redirect_uri,
        # where Spotify will send the auth code as a query parameter
        redirect_host = self.redirect_uri.split(":")[1].replace("//", "")
        redirect_port = int(self.redirect_uri.split(":")[2].split("/")[0])

        webbrowser.open(auth_url)
        # create a server to handle the request sent to the redirect_uri
        with HTTPServer((redirect_host, redirect_port), SpotifyAuthHandler) as server:
            server.handle_request()
            return server.code

    def request_access_token(self, auth_code) -> dict:
        # submit Client ID, Client Secret, and auth code to Spotify
        target_url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": "Basic " + base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode(),
            "Content-Type": "application/x-www-form-urlencoded"
        }
        payload = { 
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": self.redirect_uri
        }
        response = requests.post(target_url, headers=headers, data=payload)
        return response.json()

    def refresh_access_token(self) -> dict:
        '''
        Submit Client ID, Client Secret, and refresh token to Spotify
        to recieve a new access token.
        '''
        target_url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": "Basic " + base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode(),
            "Content-Type": "application/x-www-form-urlencoded"
        }
        payload = { 
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token
        }
        response = requests.post(target_url, headers=headers, data=payload)
        return response.json()


class SpotifyAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        self.server.code = self.path.split("=")[1]
        self.wfile.write(b"Success! You may now close this window.")
