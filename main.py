import re
import spotipy
import os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

#Open the file with the songs list
songs = open('songs.txt', 'r')

scope = "playlist-modify-public"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

#([a-z'=:\-\d]\s*)+ - ([a-z=:\-\d']\s*)+ - regular expression for this task

name = input("Input a name of the playlist: ")
description = input("Input a description of the playlist: ")

#function that search for a song with spotify api, it returns songs url if it found it else it returns none
def search_a_song(song):
    ruth_res = sp.search(song, type="track")
    if len(res := ruth_res['tracks']['items']) < 1:
        return

    res = res[0]
    print(res['uri'])
    return res['uri']

#list of all songs that must be in the playlist
songs_for_playlist = []

# iteration over the songs list and add each song to songs_for_playlist varialble
for i in songs:
    res = re.search("([a-z'=:\d]\s*)+ - ([a-z=:\d']\s*)+", i, flags=re.IGNORECASE).group(0)
    songs_for_playlist.append(search_a_song(res))

#it creates a playlist
playlist_id = sp.user_playlist_create(os.getenv("USER_NAME"), name, description=description)['id']

# delete all none values from songs_for_playlist
songs_for_playlist = [x for x in songs_for_playlist if x is not None]

sp.playlist_add_items(playlist_id, songs_for_playlist)