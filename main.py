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

#([a-z'=:\-\d]\s*)+ - ([a-z=:\-\d']\s*)+ - regular expression for this task WORK
#([a-z'=,():\-\d]\s*)+ - ([a-z=:\-\d']\s*)+ VERSION 0.2 WORK
#(?:\d+:\d\d -)* ([a-z'=,():\-\d]\s*)+ (-|/) ([a-z=:\-\d']\s*)+ VERSION 0.3

while not (name := input("Input a name of the playlist: ")):
    print("Name can't be empty, enter at least one symbol please...")

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
    try:
        res = re.search("(?:\d+:\d\d -)* ([a-z'=,():\-\d]\s*)+ (-|/) ([a-z=:\-\d']\s*)+", i, flags=re.IGNORECASE).group(0)
    except:
        continue
    songs_for_playlist.append(search_a_song(res))

#it creates a playlist
playlist = sp.user_playlist_create(os.getenv("USER_NAME"), name, description=description)
playlist_id = playlist['id']
playlist_link = playlist['uri']

# delete all none values from songs_for_playlist
songs_for_playlist = [x for x in songs_for_playlist if x is not None]

#add items to playlist
sp.playlist_add_items(playlist_id, songs_for_playlist)

#send link of the playlist to the user
print("Your playlist link: " + "https://open.spotify.com/playlist/" + playlist_id)