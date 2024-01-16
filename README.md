# tapedeck-pi

This repo is for a project built using a Raspberry Pi, an RFID reader, and the Spotify API to simulate playing music off of physical media.

## Demo

![](assets/demo.mov)

## Requirements

### Hardware:
- Raspberry Pi
- RC522 RFID Reader (~£5) (Great guide for wiring: https://pimylifeup.com/raspberry-pi-rfid-rc522/)

### Pip packages:
- RPi.GPIO
- mfrc522 (https://github.com/pimylifeup/MFRC522-python)

### Other:
- Spotify Premium

## Setup

1. Create a Spotify app: https://developer.spotify.com/dashboard

Ensure redirect URI is something like http://localhost:3000/callback

2. Create a .env with the following:
```
export PYTHONPATH="$PYTHONPATH:$PWD"
SPOTIFY_CLIENT_ID=YourSpotifyAppClientID
SPOTIFY_CLIENT_SECRET=YourSpotifyAppClientSecret
SPOTIFY_REDIRECT_URI=YourSpotifyAppRedirectURI
```
3. Run tapedeck.py, follow the CLI interface options
Note on writing IDs: the ID of the album can be located at the end of the URL when viewing the album on Spotify (eg., https://open.spotify.com/album/6eUW0wxWtzkFdaEFsTJto6)


## TODO:
- Add device initilization. Playing albums currently returns 404 if there is not already an active Spotify device.
- Add demo video


