import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv

# import client ID and secret from .env
load_dotenv()
SPOTIPY_CLIENT_ID = os.environ['SPOTIPY_CLIENT_ID']
SPOTIPY_CLIENT_SECRET = os.environ['SPOTIPY_CLIENT_SECRET']

# initialize spotipy
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(SPOTIPY_CLIENT_ID,SPOTIPY_CLIENT_SECRET))

# get artist name
artist_name = input('Input your favorite artist==> ')
print(artist_name)

# search for said artist
search_result = spotify.search(q='artist:'+artist_name,type='artist')

# get said artist's uri
artist_uri = search_result['artists']['items'][0]['uri']

# find their top tracks
artist_top_hits = spotify.artist_top_tracks(artist_uri)

# printing
print("Here is {}'s top 10 tracks:".format(artist_name))
for i in range(10):
    print('{0:>4}: {1}'.format(i + 1 ,artist_top_hits['tracks'][i]['name']))

'''
results = spotify.artist_albums(birdy_uri, album_type='album')
albums = results['items']
while results['next']:
    results = spotify.next(results)
    albums.extend(results['items'])

for album in albums:
    print(album['name'])
'''