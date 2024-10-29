import spotipy
from spotipy.oauth2 import SpotifyOAuth
from os import path as os_path
from os import makedirs as os_makedirs
from dotenv import dotenv_values
from urllib.request import urlretrieve
import time

# .env file
# ---------------------------
# SPOTIPY_CLIENT_ID='xxx'
# SPOTIPY_CLIENT_SECRET='xxx'

SPOTIPY_REDIRECT_URI="http://127.0.0.1:9090"

class SpotifyHandler:
    def __init__(self, img_dir="img"):
        scope = "user-read-playback-state user-modify-playback-state"
        env = dotenv_values(".env")

        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=env["SPOTIPY_CLIENT_ID"], client_secret=env["SPOTIPY_CLIENT_SECRET"], redirect_uri=SPOTIPY_REDIRECT_URI, scope=scope))
        self.img_dir = img_dir
        self.current_user_playing_track = None
        self.audio_features = None
        self.audio_analysis = None
        self.last_track_id = ""
        self.track_changed = False
        self.last_fetch_time = 0
        
        if not os_path.exists(self.img_dir):
            os_makedirs(self.img_dir)

    def check_beat(self, range=10) -> bool:
        """Check if a beat is happening with a range of a few milliseconds"""
        if self.current_user_playing_track is None:
            return False
        current_position = self.get_track_progress()
        for beat in self.audio_analysis["beats"]:
            if current_position < beat["start"]*1000 + range / 2 and current_position > beat["start"]*1000 - range / 2:
                return True
            
    def is_track(self):
        if self.current_user_playing_track is None:
            return False
        return self.current_user_playing_track["currently_playing_type"] == "track"

    def fetch(self):
        self.current_user_playing_track = self.sp.current_user_playing_track()


        if not self.is_track():
            return

        self.last_fetch_time = time.time()

        if self.get_track_id() != self.last_track_id:
            self.last_track_id = self.get_track_id()
            print("New Song:", self.get_track_name())
            urlretrieve(self.get_cover_url(), self.img_dir + "/cover.png")
            urlretrieve(self.get_cover_url(small=True), self.img_dir + "/cover_small.png")
            self.audio_features = self.sp.audio_features(self.get_track_id())
            self.audio_analysis = self.sp.audio_analysis(self.get_track_id())
            self.track_changed = True

    def get_artists(self) -> str:
        if not self.is_track():
            return ""
        artist_names = []
        for artist in self.current_user_playing_track['item']['artists']:
            artist_names.append(artist['name'])
        return ", ".join(artist_names)
    
    def get_cover_url(self, small=False) -> str:
        if not self.is_track():
            return ""
        if small:
            return self.current_user_playing_track['item']['album']['images'][2]['url']
        else:
            return self.current_user_playing_track['item']['album']['images'][1]['url']
        
    def get_danceability(self) -> float:
        if self.audio_features is None:
            return 0
        return self.audio_features[0]["danceability"]
    
    def get_energy(self) -> float:
        if self.audio_features is None:
            return 0
        return self.audio_features[0]["energy"]
    
    def get_time_until_next_section(self) -> float:
        if self.audio_analysis is None:
            return 0
        current_position = self.get_track_progress()
        for section in self.audio_analysis["sections"]:
            if current_position < section["start"]*1000:
                return (section["start"]*1000 - current_position) / 1000
        return 0
    
    def get_section_id(self) -> int:
        if self.audio_analysis is None:
            return 0
        current_position = self.get_track_progress()
        for id, section in enumerate(self.audio_analysis["sections"]):
            if section["start"]*1000 < current_position < section["start"]*1000 + section["duration"]*1000:
                return id
        return 0
    
    def get_section_danceability(self) -> float:
        if self.audio_analysis is None:
            return 0
        return self.audio_analysis["sections"][self.get_section_id()]["danceability"]
    
    def get_section_energy(self) -> float:
        if self.audio_analysis is None:
            return 0
        return self.audio_analysis["sections"][self.get_section_id()]["energy"]
    
    def get_section_loudness(self) -> float:
        if self.audio_analysis is None:
            return 0
        return self.audio_analysis["sections"][self.get_section_id()]["loudness"]
    
    def get_section_tempo(self) -> float:
        if self.audio_analysis is None:
            return 0
        return self.audio_analysis["sections"][self.get_section_id()]["tempo"]
    
    def get_tempo(self) -> float:
        if self.audio_features is None:
            return 0
        return self.audio_features[0]["tempo"]
        
    def get_track_id(self) -> str:
        if not self.is_track():
            return ""
        return self.current_user_playing_track["item"]["id"]

    def get_track_name(self) -> str:
        if not self.is_track():
            return ""
        return self.current_user_playing_track["item"]["name"]
    
    def get_track_progress(self) -> float:
        if not self.is_track():
            return 0
        if self.current_user_playing_track['is_playing']:
            return self.current_user_playing_track["progress_ms"] + (time.time() - self.last_fetch_time) * 1000
        else:
            return self.current_user_playing_track["progress_ms"]
        
    def has_track_changed(self) -> bool:
        if self.track_changed:
            self.track_changed = False
            return True
        return False
        
    def is_playing(self) -> bool:
        if not self.is_track():
            return False
        return self.current_user_playing_track['is_playing']
    
    def player_next(self):
        self.sp.next_track()

    def player_pause(self):
        self.sp.pause_playback()

    def player_play(self):
        self.sp.start_playback()

    def player_previous(self):
        self.sp.previous_track()
    
def main():
    spotify = SpotifyHandler()
    spotify.fetch()

if __name__ == "__main__":
    main()