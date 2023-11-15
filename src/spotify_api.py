import requests, webbrowser, base64
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlencode


class SpotifyAuth:
    '''
    Class to follow Spotify API authorization code flow per:
    https://developer.spotify.com/documentation/web-api/tutorials/code-flow

    This auth flow will allow playback. Needed from the user are the Spotify
    application Client ID, Client Secret, and Redirect URI. These can be
    found in the app settings from https://developer.spotify.com/dashboard
    '''
    def __init__(self, client_id, redirect_uri, client_secret) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        auth_code = self.request_auth_code(self.request_auth_url())
        tokens = self.request_access_token(auth_code)
        self.access_token = tokens["access_token"]
        self.refresh_token = tokens["refresh_token"]


    def request_auth_url(self) -> str:
        ''' 
        Submit Client ID and Redirect URI to Spotify to recieve the
        authroization URL that the user is meant to use to authenticate.
        - reponse_type is always "code"
        - only user-modify-playback-state scope needed for this application
        '''
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
        '''
        Open the authorization URL retrieved from get_auth_url() in
        the web browser. User will click to authentcate, which will make
        Spotify send a request to the specified Redirect URI. Listen
        on the specified Redirect URI for that request and retrieve
        the authorization code from it. 
        '''
        redirect_host = self.redirect_uri.split(":")[1].replace("//", "")
        redirect_port = int(self.redirect_uri.split(":")[2].split("/")[0])

        webbrowser.open(auth_url)
        with HTTPServer((redirect_host, redirect_port), SpotifyAuthHandler) as server:
            server.handle_request()
            return server.code
        

    def request_access_token(self, auth_code) -> dict:
        '''
        Submit Client ID, Client Secret, and authorization code to Spotify
        to recieve the access token that will be used to make requests to
        the API.
        '''
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
    '''
    Extend BaseHTTPRequestHandler to handle the request sent to the 
    redirect URI by Spotify during the authorization code flow,
    capture and store the auth code.
    '''
    def do_GET(self) -> None:
        self.server.code = self.path.split("=")[1]
        self.wfile.write(b"Success! You may now close this window.")
        

class SpotifyAPI:
    '''
    Class to interact with the Spotify API per 
    https://developer.spotify.com/documentation/web-api/
    Uses access token gained from SpotifyAuth class.
    '''
    def __init__(self, access_token) -> None:
        self.base_url = "https://api.spotify.com/v1"
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {access_token}"})
    

    def play(self, id, type) -> dict:
        '''
        Play a track, album, or playlist. Requires ID of the item to play 
        (retrieved from the end of a share link) and the type of item
        TODO: Add support for no active device
        '''
        response = self.session.put(f"{self.base_url}/me/player/play",
            json = {
                "context_uri": self.id_to_uri(id=id, type=type)
            }
        )
        if response.status_code != 200:
            raise KeyError(f"Could not play. Check your URI. \n Response: {response.json()}")

        return response.json()
    

    def id_to_uri(self, id, type) -> str:
        '''
        Convert an ID to a Spotify URI.
        '''
        if type in ["album", "artist", "playlist", "track"]:
            return f"spotify:{type}:{id}"
        
        raise ValueError(f"Type must be of album, artist, playlist, or track. Received {type}")
    

    def uri_to_id(self, uri) -> str:
        '''
        Convert a Spotify URI to an ID.
        '''
        return uri.split(":")[2]
