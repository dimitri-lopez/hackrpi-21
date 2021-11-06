# -*- coding: utf-8 -*-
"""
Created on Sat Nov  6 12:02:50 2021

@author: Huy Chu
"""

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from config import CLIENT_ID, CLIENT_SECRET


auth_manager = SpotifyClientCredentials(CLIENT_ID,CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

playlists = sp.user_playlists('spotify')
while playlists:
    for i, playlist in enumerate(playlists['items']):
        print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None