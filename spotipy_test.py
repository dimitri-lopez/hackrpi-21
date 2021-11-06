import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv
import pandas

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
if len(search_result['artists']['items']) > 0:
    artist_uri = search_result['artists']['items'][0]['uri']
else:
    print('Artist not found!')
    exit()


album_result = spotify.artist_albums(artist_uri)
artist_all_album = album_result['items']
# print(len(artist_all_album))
# print(spotify.album_tracks(artist_all_album[0]['id']))

'''
artist_all_songs = []
for album in artist_all_album:
    tracks_result = spotify.album_tracks(album['id'])
    artist_all_songs.extend(tracks_result['items'])
    while tracks_result['next']:
        tracks_result = spotify.next(tracks_result)
        artist_all_songs.extend(tracks_result['items'])

for song in artist_all_songs:
    print(song['name'])
'''

def album_to_panda(album):
    
    # get all tracks in the album
    album_tracks_result = spotify.album_tracks(album['id'])
    album_songs = album_tracks_result['items']
    while album_tracks_result['next']:
        album_tracks_result = spotify.next(album_tracks_result)
        album_songs.extend(album_tracks_result['items'])
    
    song_ids = [album_songs[x]['id'] for x in range(len(album_songs))]

    audio_feature_res = spotify.audio_features(song_ids)

    panda_df = {}

    panda_df['name'] = []
    panda_df['duration'] = []
    panda_df['date'] = []
    panda_df['tempo'] = []
    panda_df['energy'] = []
    panda_df['valence'] = []

    # print(album_songs[0])

    for i in range(len(album_songs)):
        panda_df['name'].append(album_songs[i]['name'])
        panda_df['duration'].append(album_songs[i]['duration_ms'])
        panda_df['date'].append(album['release_date'])
        panda_df['tempo'].append(audio_feature_res[i]['tempo'])
        panda_df['energy'].append(audio_feature_res[i]['energy'])
        panda_df['valence'].append(audio_feature_res[i]['valence'])

    df = pandas.DataFrame(data=panda_df)
    return df

for album in artist_all_album:
    print(album_to_panda(album))

'''
# find their top tracks
artist_top_hits = spotify.artist_top_tracks(artist_uri)

# printing
print("Here is {}'s top tracks:".format(artist_name))
for i in range(min(len(artist_top_hits['tracks']),10)):
    print('{0:>4}: {1}'.format(i + 1 ,artist_top_hits['tracks'][i]['name']))
'''

'''
results = spotify.artist_albums(birdy_uri, album_type='album')
albums = results['items']
while results['next']:
    results = spotify.next(results)
    albums.extend(results['items'])

for album in albums:
    print(album['name'])
'''