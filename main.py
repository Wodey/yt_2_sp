import re
import spotipy
import os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

songs = open('songs.txt', 'r')

auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)

#([a-z'=:\d]\s*)+ - ([a-z=:\d']\s*)+ - regular expression for this(may has some problems with matches groups

def search_a_song(song):
    ruth_res = sp.search(song, type="track")
    if len(res := ruth_res['tracks']['items']) < 1:
        print("Can't find a track")
        return

    res = res[0]

    print(res['uri'])
    return res['uri']

for i in songs:
    res = re.search("([a-z'=:\d]\s*)+ - ([a-z=:\d']\s*)+", i, flags=re.IGNORECASE).group(0)
    search_a_song(res)


