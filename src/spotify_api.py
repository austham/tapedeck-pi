
import requests


class SpotifyAPI:
    def __init__(self, client_id, client_secret):
        self.auth_token = self.get_auth_token(client_id, client_secret)
        self.auth_header = {'Authorization' : f'Bearer {self.auth_token}'}
        self.base_url = 'https://api.spotify.com/v1'


    def get_auth_token(self, client_id, client_secret):

        response = requests.post('https://accounts.spotify.com/api/token',
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data = {
                'grant_type': 'client_credentials',
                'client_id': client_id,
                'client_secret': client_secret
            }
        )
        if response.status_code != 200:
            raise KeyError(f"Could not get Spotify auth token. Check your client ID and client secret. \n Response: {response}")

        return response.json()['access_token']


    def get_album(self, id):

        response = requests.get(f'{self.base_url}/albums/{id}',
            headers = self.auth_header
        )
        if response.status_code != 200:
            raise KeyError(f"Could not get album. Check your album ID. \n Response: {response}")

        return response.json()
    

    def play(self, uri):
        response = requests.put(f'{self.base_url}/me/player/play',
            headers = self.auth_header,
            json = {
                'context_uri': uri
            }
        )
        if response.status_code != 200:
            raise KeyError(f"Could not play. Check your URI. \n Response: {response}")

        return response.json()
    

    def id_to_uri(self, id, type):

        if type in ['album', 'artist', 'playlist', 'track']:
            return f'spotify:{type}:{id}'
        
        raise ValueError(f'Type must be of album, artist, playlist, or track. Received {type}')
