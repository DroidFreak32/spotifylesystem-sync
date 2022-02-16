import spotipy
from spotipy import SpotifyOAuth

SPOTIPY_CLIENT_ID = "327d9a61415f4e98b36a8964485e7f41"
SPOTIPY_CLIENT_SECRET = "2909fdb6d8a148bd950fcf4298e0f30e"
redirect_uri = "http://127.0.0.1:9090"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=redirect_uri,
                                               scope="user-library-read playlist-modify-private"))


def show_tracks(results):
    for item in results['items']:
        track = item['track']
        print("%32.32s %s" % (track['artists'][0]['name'], track['name']))


results = sp.current_user_saved_tracks()
show_tracks(results)

while results['next']:
    results = sp.next(results)
    show_tracks(results)
