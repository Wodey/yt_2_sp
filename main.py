import re

songs = open('songs.txt', 'r')

#([a-z'=:\d]\s*)+ - ([a-z=:\d']\s*)+ - regular expression for this(may has some problems with matches groups

for i in songs:
    res = re.search("([a-z'=:\d]\s*)+ - ([a-z=:\d']\s*)+", i, flags=re.IGNORECASE)
    print(res.group(0))

