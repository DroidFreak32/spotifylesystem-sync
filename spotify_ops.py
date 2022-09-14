from datetime import datetime

import tqdm

from common import get_spotify_connection, bcolors

sp = get_spotify_connection()


def get_missing_playlist_items_from_trackids(playlist_id=None, track_ids=None):
    """
    For some unknown reason not all tracks gets added in the playlist.
    In such cases return the missing track IDs back to the calling function
    """
    _, playlist_tracks = get_playlist(playlist_id=playlist_id)
    if len(playlist_tracks) == len(track_ids):
        return None
    missing_playlist_items = []
    playlist_track_ids = []
    for playlist_track in playlist_tracks:
        playlist_track_ids.append(playlist_track['SPOTIFY'][-22:])
    for track_id in track_ids:
        if track_id not in playlist_track_ids:
            missing_playlist_items.append(track_id)
    return missing_playlist_items


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
        if track['ALBUMARTIST'] == 'Various Artists':
            track['ALBUMARTIST'] = get_proper_albumartist(item['track']['artists'])
        cleaned_playlist.append(track)
    return cleaned_playlist


def get_playlist_tracks(selected_playlist_id, selected_playlist_tracktotal):
    offset = 0
    loops = int(selected_playlist_tracktotal / 100) + 1

    if loops % 100 == 0:
        loops -= 1

    full_playlist_raw = []
    for i in range(loops):
        playlist_raw = sp.playlist_items(playlist_id=selected_playlist_id, offset=offset,
                                         fields='items.track.album.artists.name,'
                                                'items.track.album.name,'
                                                'items.track.artists,'
                                                'items.track.name,'
                                                'items.track.external_urls.spotify',
                                         additional_types=['track'])['items']
        full_playlist_raw += playlist_raw
        offset += 100
        print(f"Retrieved {offset} / {selected_playlist_tracktotal} tracks from playlist.", end="\r", flush=True)

    return cleanup_playlist(full_playlist_raw)


############################################
# Externally callable functions start here #
############################################

def get_playlist(playlist_id=None):
    # results = sp.current_user_saved_tracks()
    # for idx, item in enumerate(results['items']):
    #     track = item['track']
    #     print(idx, track['artists'][0]['name'], " – ", track['name'])

    if playlist_id is None:
        playlist_list = sp.current_user_playlists(limit=50)
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
    else:
        playlist = sp.playlist(playlist_id)
        selected_playlist_id = playlist_id
        selected_playlist_name = playlist['name']
        selected_playlist_tracktotal = playlist['tracks']['total']
        selected_playlist_tracks = get_playlist_tracks(selected_playlist_id, selected_playlist_tracktotal)
    return selected_playlist_name, selected_playlist_tracks


def get_user_playlists(user_id=None, playlist_id=None):
    if user_id is None:
        print("No user ID provided, using the current authenticated user's ID")
        user_id = sp.me()['id']
    if playlist_id is None:
        playlist_limited_batch = sp.user_playlists(user=user_id, limit=50)
        total_playlists = playlist_limited_batch['total']
        offset = 0
        playlist_list = dict()
        while offset < total_playlists:
            for item in playlist_limited_batch['items']:
                # Every playlist has a unique ID which we can use as the key without worrying about appending logic
                # to a list
                playlist_list[item['id']] = (item['name'], item['tracks']['total'])
            offset += 50
            playlist_limited_batch = sp.next(playlist_limited_batch)

        print("Playlists found in your account:")
        for key, value in playlist_list.items():
            print("ID: {:<10} Name: {:<40} Total Tracks: {:<15}".format(key, value[0], value[1]))

        selected_playlist_id = input("Enter the playlist ID: ")

        selected_playlist_name = playlist_list[selected_playlist_id][0]
        selected_playlist_tracktotal = playlist_list[selected_playlist_id][1]
        selected_playlist_tracks = get_playlist_tracks(selected_playlist_id, selected_playlist_tracktotal)
    else:
        playlist = sp.playlist(playlist_id)
        selected_playlist_id = playlist_id
        selected_playlist_name = playlist['name']
        selected_playlist_tracktotal = playlist['tracks']['total']
        selected_playlist_tracks = get_playlist_tracks(selected_playlist_id, selected_playlist_tracktotal)

    return selected_playlist_name, selected_playlist_tracks


def get_my_saved_tracks():
    results = sp.current_user_saved_tracks()
    total_tracks = results['total']
    offset = 0
    results_raw = []
    # Results is a dict with key next indicating offset.
    # Only 20 tracks can be retrieved per API call.
    with tqdm.tqdm(total=total_tracks, desc="Loading tracks") as pbar:
        while offset < total_tracks:
            for item in results['items']:
                results_raw += [{'track': item['track']}]
            pbar.update(20)
            offset += 20
            # print(f"Retrieving {offset+20} / {total_tracks} tracks.", end="\r", flush=True)
            results = sp.next(results)
    all_my_tracks = cleanup_playlist(playlist_raw=results_raw)
    missing_tracks_playlist_name = sp.me()['display_name'] + "'s missing tracks"
    return missing_tracks_playlist_name, all_my_tracks


def generate_missing_track_playlist(unmatched_track_ids=None, playlist_name=None, playlist_id=None):
    if unmatched_track_ids is None:
        unmatched_track_ids = []
    total_tracks = len(unmatched_track_ids)
    offset = 0
    loops = int(total_tracks / 10) + 1

    if loops % 10 == 0:
        loops -= 1

    user_id = sp.me()['id']
    if playlist_name is None:
        playlist_name = "Missing_spotifyle_" + datetime.today().strftime('%Y%m%d_%H%M')
    else:
        playlist_name = playlist_name + ' - ' + datetime.today().strftime('%Y%m%d_%H%M')

    if playlist_id is None:
        new_playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
        playlist_id = new_playlist['id']

    for i in range(loops):
        print(f"Creating playlist {playlist_name}: {offset}/{total_tracks} tracks", end="\r")
        current_batch_of_tracks = unmatched_track_ids[offset:offset + 10]
        sp.playlist_add_items(playlist_id=playlist_id, items=current_batch_of_tracks)
        offset += 10

    missing_playlist_items = get_missing_playlist_items_from_trackids(
        playlist_id=playlist_id, track_ids=unmatched_track_ids)

    if missing_playlist_items is not None:
        print(f"Few Tracks Missing")
        generate_missing_track_playlist(
            unmatched_track_ids=missing_playlist_items, playlist_name=playlist_name, playlist_id=playlist_id)
    print(f"Playlist: {playlist_name} created!")

    return None


if __name__ == '__main__':
    # generate_missing_track_playlist(unmatched_track_ids=unmatched_track_ids)
    # get_playlist()
    my_tracks = get_my_saved_tracks()
    print("K")
