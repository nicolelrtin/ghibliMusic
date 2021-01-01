from __future__ import unicode_literals

# pip install spotipy
import spotipy
import spotipy.oauth2 as oauth2
from spotipy.oauth2 import SpotifyClientCredentials

# pip install youtube-search-python
from youtubesearchpython import VideosSearch

# pip install youtube_dl
import youtube_dl

# Confirm credentials
cid = ''
secret = ''
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

credentials = oauth2.SpotifyClientCredentials(
    client_id=cid,
    client_secret=secret)
token = credentials.get_access_token(as_dict=False)
spotify = spotipy.Spotify(auth=token)


# search songs by artist
def artist_tracks(artist):
    tracks = []
    results = spotify.search(q='artist:' + artist, type='track')['tracks']['items']
    for i in range(len(results)):
        try:
            tracks += [results[i]['name']]
        except IndexError: pass
    return tracks


# grab all songs in playlist (use first result)
def playlist_tracks(playlist_name):
    search = spotify.search(q=playlist_name, type='playlist')['playlists']['items'][0]
    playlist = spotify.user_playlist(search['owner']['id'], search['id'])
    results = playlist['tracks']['items']
    tracks = []
    for i in range(len(results)):
        tracks += [results[i]['track']['name']]
    return tracks


# return lst of youtube links from list of songs
def song2wav(tracks):
    links = []
    for title in tracks:
        video_res = VideosSearch(title, limit=1)
        links += [video_res.result().get('result')[0].get('link')]

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        [ydl.download([link]) for link in links]


song2wav(artist_tracks('hisaishi'))
