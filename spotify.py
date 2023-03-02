import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import dotenv_values
import urllib.request

# .env file
# ---------------------------
# SPOTIPY_CLIENT_ID='xxx'
# SPOTIPY_CLIENT_SECRET='xxx'

env = dotenv_values(".env")

SPOTIPY_REDIRECT_URI='http://127.0.0.1:9090'

class Spotify:
    def __init__(self):
        scope = "user-read-playback-state"
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=env["SPOTIPY_CLIENT_ID"], client_secret=env["SPOTIPY_CLIENT_SECRET"], redirect_uri=SPOTIPY_REDIRECT_URI, scope=scope))
        self.track_title = "Waiting for fetch..."
        self.track_cover_url = ""
        self.track_artist = ""

    def fetch(self):
        results = self.sp.current_playback(market=None, additional_types=None)

        self.track_title = results['item']['name']

        self.track_cover_url = results['item']['album']['images'][1]['url']
        urllib.request.urlretrieve(self.track_cover_url, "img/cover.png")

        artist_names = []
        for artist in results['item']['artists']:
            artist_names.append(artist['name'])
        self.track_artist = ", ".join(artist_names)
