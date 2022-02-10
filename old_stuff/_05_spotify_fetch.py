import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint

from global_vars import sp


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def get_proper_albumartist(artist_list=None):
    """
    Multiple Album artists should not exist. Artist tag should be used for featured artists.
    :param artist_list:
    :return: 1st name in AlbumArtists
    """
    if len(artist_list) > 1:
        print(f"\n{bcolors.FAIL}Multiple Album Artists in track.\n"
              f"Only storing the first one: {artist_list[0]['name']}{bcolors.ENDC}")

    return artist_list[0]['name']


def get_proper_artist(artist_list=None):
    """
    Helper to lookup all available artists
    :param artist_list:
    :return: Either a string or a list of artists
    """
    if len(artist_list) == 1:
        alist = artist_list[0]['name']
    else:
        alist = []
        for artist in artist_list:
            alist.append(artist['name'])
    return alist


def cleanup_playlist(playlist_raw=None):
    """
    Cleans up unnecessary cruft from spotify playlist objects like urls, thumbnails, added_at etc
    :param playlist_raw: raw Spotify playlist object
    :return: Cleaned up list of tracks in provided playlist.
    Each item contains the track's TITLE, ALBUM, ALBUMARTIST, ARTIST & SPOTIFY URI
    """

    cleaned_playlist = []
    for item in playlist_raw:
        track = dict()
        track['ALBUMARTIST'] = get_proper_albumartist(item['track']['album']['artists'])
        track['ALBUM'] = item['track']['album']['name']
        track['TITLE'] = item['track']['name']
        track['ARTIST'] = get_proper_artist(item['track']['artists'])
        track['SPOTIFY'] = item['track']['external_urls']['spotify']
        cleaned_playlist.append(track)
    return cleaned_playlist


def get_playlist_tracks(selected_playlist_id, selected_playlist_tracktotal):
    offset = 0
    playlist_raw = sp.playlist_items(playlist_id=selected_playlist_id, offset=offset,
                                     fields='items.track.album.artists.name,items.track.album.name,items.track.artists,'
                                            'items.track.name,items.track.external_urls.spotify',
                                     additional_types=['track'])
    full_playlist_raw = playlist_raw
    offset = offset + len(playlist_raw['items'])
    while True:
        playlist_raw = sp.playlist_items(playlist_id=selected_playlist_id, offset=offset,
                                         fields='items.track.album.artists.name,items.track.album.name,items.track.artists,'
                                                'items.track.name,items.track.external_urls.spotify',
                                         additional_types=['track'])

        if len(playlist_raw['items']) == 0:
            break

        full_playlist_raw['items'].extend(playlist_raw['items'])
        print(f"Fetched {offset} / {selected_playlist_tracktotal} tracks", end='\r')
        offset = offset + len(playlist_raw['items'])

    return cleanup_playlist(full_playlist_raw['items'])


def main():

    # results = sp.current_user_saved_tracks()
    # for idx, item in enumerate(results['items']):
    #     track = item['track']
    #     print(idx, track['artists'][0]['name'], " – ", track['name'])

    playlist_list = sp.current_user_playlists()
    items = playlist_list['items']
    playlist_ids = dict()
    for item in items:
        # Create a dictionary of format { 'ID': (name, total tracks), ... }
        playlist_ids[item['id']] = (item['name'], item['tracks']['total'])

    print("Playlists found in your account:")
    for key, value in playlist_ids.items():
        print("ID: {:<10} Name: {:<40} Total Tracks: {:<15}".format(key, value[0], value[1]))

    selected_playlist_id = input("Enter the playlist ID: ")
    selected_playlist_name = playlist_ids[selected_playlist_id][0]
    selected_playlist_tracktotal = playlist_ids[selected_playlist_id][1]
    selected_playlist_tracks = get_playlist_tracks(selected_playlist_id, selected_playlist_tracktotal)

    return selected_playlist_tracks


if __name__ == '__main__':
    main()
