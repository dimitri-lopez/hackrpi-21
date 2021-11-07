import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv
import pandas as pd


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
    panda_df['album name'] = []

    # update song dictionary
    for i in range(len(album_songs)):
        panda_df['name'].append(album_songs[i]['name'])
        panda_df['duration'].append(album_songs[i]['duration_ms'])
        panda_df['date'].append(album['release_date'])
        panda_df['tempo'].append(audio_feature_res[i]['tempo'])
        panda_df['energy'].append(audio_feature_res[i]['energy'])
        panda_df['valence'].append(audio_feature_res[i]['valence'])
        panda_df['album name'].append(album['name'])
    # creating dataframe from song dict
    df = pd.DataFrame(data=panda_df)
    return df

def artist_top_songs(artist):
    artist_top_hits = spotify.artist_top_tracks(artist['id'])
    artist_top_hits = artist_top_hits['tracks']
    
    song_ids = [artist_top_hits[x]['id'] for x in range(len(artist_top_hits))]
    audio_feature_res = spotify.audio_features(song_ids)
    panda_df = {}

    panda_df['name'] = []
    panda_df['duration'] = []
    panda_df['date'] = []
    panda_df['tempo'] = []
    panda_df['energy'] = []
    panda_df['valence'] = []
    panda_df['album name'] = []

    # update song dictionary
    for i in range(len(artist_top_hits)):
        album_id = artist_top_hits[i]['album']['id']
        album_of_song = spotify.album(album_id)
        panda_df['name'].append(artist_top_hits[i]['name'])
        panda_df['duration'].append(artist_top_hits[i]['duration_ms'])
        panda_df['date'].append(album_of_song['release_date'])
        panda_df['tempo'].append(audio_feature_res[i]['tempo'])
        panda_df['energy'].append(audio_feature_res[i]['energy'])
        panda_df['valence'].append(audio_feature_res[i]['valence'])
        panda_df['album name'].append(album_of_song['name'])
    # creating dataframe from song dict
    df = pd.DataFrame(data=panda_df)
    return df

def look_up_artist(artist_name):
    # {} parameter: string
    # search for said artist
    search_result = spotify.search(q='artist:'+artist_name, type='artist')

    # get said artist's uri
    if len(search_result['artists']['items']) > 0:
        artist_obj = search_result['artists']['items'][0]
        artist_uri = artist_obj['uri']
    else:
        # print('Artist not found!')
        return None

    top_ten_df = artist_top_songs(artist_obj)

    if len(artist_obj['images']) > 0:
        artist_img_url = artist_obj['images'][0]['url']
    else:
        artist_img_url = ''
    artist_info = [artist_obj['name'], ', '.join(artist_obj['genres']), artist_img_url, artist_obj['external_urls']['spotify']]

    album_result = spotify.artist_albums(artist_uri)
    artist_all_album = album_result['items']

    albums = []
    for album in artist_all_album:
        albums.append(album_to_panda(album))
    df = pd.concat(albums, ignore_index = True).drop_duplicates("name")
    return [df,artist_info,top_ten_df]


# import client ID and secret from .env
load_dotenv()
SPOTIPY_CLIENT_ID = os.environ['SPOTIPY_CLIENT_ID']
SPOTIPY_CLIENT_SECRET = os.environ['SPOTIPY_CLIENT_SECRET']

# initialize spotipy
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
    SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET))

if __name__ == '__main__':
    artist_name = "dodie"
    res = look_up_artist(artist_name)
    print(res[0])
    print(res[1])
    print(res[2])
