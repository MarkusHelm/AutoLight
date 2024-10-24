import spotipy
from spotipy.oauth2 import SpotifyOAuth
from os import path as os_path
from os import makedirs as os_makedirs
from dotenv import dotenv_values
from urllib.request import urlretrieve

# .env file
# ---------------------------
# SPOTIPY_CLIENT_ID='xxx'
# SPOTIPY_CLIENT_SECRET='xxx'

SPOTIPY_REDIRECT_URI="http://127.0.0.1:9090"

class SpotifyHandler:
    def __init__(self, img_dir="img"):
        scope = "user-read-playback-state"
        env = dotenv_values(".env")

        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=env["SPOTIPY_CLIENT_ID"], client_secret=env["SPOTIPY_CLIENT_SECRET"], redirect_uri=SPOTIPY_REDIRECT_URI, scope=scope))
        self.img_dir = img_dir
        self.results = None
        self.last_track_id = ""
        self.track_changed = False
        
        if not os_path.exists(self.img_dir):
            os_makedirs(self.img_dir)

    def fetch(self):
        self.results = self.sp.current_user_playing_track()

        if self.results is None:
            return

        if self.get_track_id() != self.last_track_id:
            self.last_track_id = self.get_track_id()
            print("New Song:", self.get_track_name())
            urlretrieve(self.get_cover_url(), self.img_dir + "/cover.png")
            urlretrieve(self.get_cover_url(small=True), self.img_dir + "/cover_small.png")
            self.track_changed = True

    def get_track_id(self) -> str:
        if self.results is None:
            return ''
        return self.results["item"]["id"]

    def get_track_name(self) -> str:
        if self.results is None:
            return ''
        return self.results["item"]["name"]
    
    def get_artists(self) -> str:
        if self.results is None:
            return ''
        artist_names = []
        for artist in self.results['item']['artists']:
            artist_names.append(artist['name'])
        return ", ".join(artist_names)
    
    def get_cover_url(self, small=False) -> str:
        if self.results is None: return ''
        if small:
            return self.results['item']['album']['images'][2]['url']
        else:
            return self.results['item']['album']['images'][1]['url']
        
    def has_track_changed(self) -> bool:
        if self.track_changed:
            self.track_changed = False
            return True
        return False
        
    def is_playing(self) -> bool:
        if self.results is None:
            return False
        return self.results['is_playing']
    