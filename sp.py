import re
import spotipy
import os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()


class SpotifyController:
    def __init__(self):
        scope = "playlist-modify-public"
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
        self.songs = []

    # function that search for a song with spotify api, it returns songs url if it found it else it returns none
    def search_a_song(self, song):
        ruth_res = self.sp.search(song, type="track")
        if len(res := ruth_res['tracks']['items']) < 1:
            return

        res = res[0]
        print(res['uri'])
        return res['uri']

    def parse_text_and_find_songs(self, text):
        # iteration over the songs list and add each song to songs_for_playlist varialble
        print(text)
        for i in text.split("\n"):
            try:
                res = re.search("(?:\d+:\d\d -)* (([a-z'=,(’&):\-\d]\s*)+ (-|/) ([a-z=’:&\-\d']\s*)+)+", i,
                                flags=re.IGNORECASE).group(1)
            except:
                continue

            self.songs.append(self.search_a_song(res))

        if not self.songs:
            return 1

    def create_a_playlist(self, name, description):
        # it creates a playlist
        playlist = self.sp.user_playlist_create(os.getenv("USER_NAME"), name, description=description)
        playlist_id = playlist['id']
        playlist_link = playlist['uri']

        # delete all none values from songs_for_playlist
        songs_for_playlist = [x for x in self.songs if x is not None]

        # add items to playlist
        self.sp.playlist_add_items(playlist_id, songs_for_playlist)

        return "https://open.spotify.com/playlist/" + playlist_id
