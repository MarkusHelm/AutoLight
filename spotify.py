import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import dotenv_values
import urllib.request
import os

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
        self.results = None
        self.lastTrackId = ''
        
        if not os.path.exists('img'):
            os.makedirs('img')

    def update(self):
        self.results = self.sp.current_user_playing_track()

        if self.results is None:
            return None

        if self.getTrackId() != self.lastTrackId:
            self.lastTrackId = self.getTrackId()
            print("New Song:", self.getTrackName())
            urllib.request.urlretrieve(self.getCoverUrl(), "img/cover.png")
            urllib.request.urlretrieve(self.getCoverUrl(small=True), "img/cover_small.png")
            return True
        
        return False

    def getTrackId(self) -> str:
        if self.results is None: return ''
        return self.results["item"]["id"]

    def getTrackName(self) -> str:
        if self.results is None: return ''
        return self.results["item"]["name"]
    
    def getArtists(self) -> str:
        if self.results is None: return ''
        artist_names = []
        for artist in self.results['item']['artists']:
            artist_names.append(artist['name'])
        return ", ".join(artist_names)
    
    def getCoverUrl(self, small=False) -> str:
        if self.results is None: return ''
        if small == True:
            return self.results['item']['album']['images'][2]['url']
        else:
            return self.results['item']['album']['images'][1]['url']
    