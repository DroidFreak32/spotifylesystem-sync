import time
from datetime import datetime

import tqdm

from common import get_spotify_connection, bcolors

sp = get_spotify_connection()


def get_missing_playlist_items_from_trackids(playlist_id=None, track_ids=None):
    """
    For some unknown reason not all tracks gets added in the playlist.
    In such cases return the missing track IDs back to the calling function
    """
    _, playlist_tracks = get_user_playlists(playlist_id=playlist_id)
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


def get_proper_artist_str_or_list(artist_list=None):
    """
    Helper to lookup all available artists
    :param artist_list:
    :return: Either a string or a list of artists
    """
    if len(artist_list) == 1:
        alist = [artist_list[0]['name']]
    else:
        alist = []
        for artist in artist_list:
            alist.append(artist['name'])
    return alist


def get_proper_artist(artist_list=None):
    """
    Helper to lookup all available artists
    :param artist_list:
    :return: Artist names in a list
    """
    if len(artist_list) == 1:
        return [artist_list[0]['name']]
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
        # BUG: Local tracks crash this method, skip them.
        if item['track']['is_local']:
            continue
        track = dict()
        track['ALBUMARTIST'] = get_proper_albumartist(item['track']['album']['artists'])
        track['ALBUM'] = item['track']['album']['name']
        track['TITLE'] = item['track']['name']
        track['ARTIST'] = get_proper_artist(item['track']['artists'])
        track['SPOTIFY'] = item['track']['external_urls']['spotify']
        track['SPOTIFY_TID'] = item['track']['id']
        if track['ALBUMARTIST'] == 'Various Artists':
            track['ALBUMARTIST'] = get_proper_albumartist(item['track']['artists'])
        cleaned_playlist.append(track)
    return cleaned_playlist


def get_playlist_tracks(selected_playlist_id, selected_playlist_tracktotal=None):
    if selected_playlist_tracktotal is None:
        selected_playlist_tracktotal = sp.playlist_items(selected_playlist_id, fields='total')['total']

    offset = 0
    loops = int(selected_playlist_tracktotal / 100) + 1

    if loops % 100 == 0:
        loops -= 1

    full_playlist_raw = []
    for i in range(loops):
        # BUG: Local tracks crash this method, capture them.
        playlist_raw = sp.playlist_items(playlist_id=selected_playlist_id, offset=offset,
                                         fields='items.track.album.artists.name,'
                                                'items.track.album.name,'
                                                'items.track.artists,'
                                                'items.track.id,'
                                                'items.track.is_local,'
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

def get_user_playlists(user_id=None, playlist_id=None, list_only=False):
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
                playlist_list[item['id']] = \
                    (item['name'], item['tracks']['total'], item['owner']['display_name'], item['owner']['id'])

            offset += 50
            playlist_limited_batch = sp.next(playlist_limited_batch)

        if list_only:
            playlist_list_only = []
            for key in playlist_list.keys():
                playlist_list_only.append(key)
            return playlist_list_only

        my_playlists_only = None
        if 'm' == str(input('Enter "M" to only view playlists created by you: \n')).casefold():
            my_playlists_only = True
        print("Playlists found in your account:")
        for key, value in playlist_list.items():
            if my_playlists_only and value[3] != user_id:
                continue
            print("ID: {:<22} Tracks:{:<5} By:{:<15} Name: {:<22}"
                  .format(key, value[1], value[2][:15], value[0][:22] + '..'))

        playlist_id = input("Enter the playlist ID: ")

        if playlist_id.casefold() == 'q':
            exit(1)

        # selected_playlist_name = playlist_list[selected_playlist_id][0]
        # selected_playlist_tracktotal = playlist_list[selected_playlist_id][1]
        # selected_playlist_tracks = get_playlist_tracks(selected_playlist_id, selected_playlist_tracktotal)
    # else:
    playlist = sp.playlist(playlist_id)
    selected_playlist_id = playlist_id
    selected_playlist_name = playlist['name']
    selected_playlist_tracktotal = playlist['tracks']['total']
    selected_playlist_tracks = get_playlist_tracks(selected_playlist_id, selected_playlist_tracktotal)

    return selected_playlist_name, selected_playlist_tracks


def fetch_user_playlists(user_id=None, owner_only=False, ids_only=False):
    if user_id is None:
        print("No user ID provided, using the current authenticated user's ID")
        user_id = sp.me()['id']

    playlist_limited_batch = sp.user_playlists(user=user_id, limit=50)
    total_playlists = playlist_limited_batch['total']
    offset = 0
    playlist_list = dict()
    while offset < total_playlists:
        for item in playlist_limited_batch['items']:
            # Every playlist has a unique ID which we can use as the key without worrying about appending logic
            # to a list
            playlist_list[item['id']] = \
                (item['name'], item['tracks']['total'], item['owner']['display_name'], item['owner']['id'])

        offset += 50
        playlist_limited_batch = sp.next(playlist_limited_batch)

    for key, value in list(playlist_list.items()):
        if owner_only and value[3] != user_id:
            playlist_list.pop(key)

    if ids_only:
        playlist_ids_only = []
        for key in playlist_list.keys():
            playlist_ids_only.append(key)
        # return playlist_ids_only
        return playlist_list.keys()

    return playlist_list


def select_user_playlist(user_id=None, owner_only=None):
    if user_id is None:
        user_id = sp.me()['id']
    if owner_only is None:
        if 'y' == str(input('Enter "Y" to only view playlists created by user: \n')).casefold():
            owner_only = True
    playlists = fetch_user_playlists(user_id, owner_only, ids_only=False)
    print("Playlists found:")
    print("****************")
    index = 1
    for key, value in playlists.items():
        print("{:<3}) ID: {:<22} Tracks:{:<5} By:{:<15} Name: {:<22}"
              .format(index, key, value[1], value[2][:15], value[0][:22] + '..'))
        index += 1

    answer = input("Enter the playlist ID: ")
    if answer.isnumeric():
        playlist_id = list(playlists.keys())[int(answer) - 1]
    else:
        playlist_id = answer
    return playlist_id


def fetch_playlist_tracks(user_id=None, playlist_id=None, owner_only=False):
    if user_id is None:
        user_id = sp.me()['id']
    if playlist_id is None:
        playlist_id = select_user_playlist(user_id=user_id, owner_only=owner_only)

    playlist = sp.playlist(playlist_id=playlist_id)
    playlist_name = playlist['name']
    playlist_tracktotal = playlist['tracks']['total']
    playlist_tracks = get_playlist_tracks(playlist_id, playlist_tracktotal)

    return playlist_name, playlist_tracks


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

    if total_tracks % 10 == 0:
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


def playlists_containing_track(track_id=None, playlist_list=None):
    """
    Returns a list of playlist that contains a particular track ID
    @param track_id: ID of the track from spotify's URL.
    Ex: URL: https://open.spotify.com/track/0lkQOB949M2gLyut86aJ1b?si=5b3b7ecd2ad44a2a
        track_id: 0lkQOB949M2gLyut86aJ1b
    @param playlist_list: A list of spotify Playlist IDs to search, defaults to all saved playlists.
    @return: A list of user's saved spotify playlists' IDs that have the track.
    """
    matched_list = []
    if track_id is None:
        track_id = input("Enter Spotify track's ID")
    if playlist_list is None:
        playlist_list = get_user_playlists(list_only=True)
    cooldown = 0
    for playlist in playlist_list:
        cooldown += 1
        tracks = get_playlist_tracks(selected_playlist_id=playlist)

        # Cooldown every 5 iterations to avoid TOO many API requests
        if not (cooldown % 5):
            # time.sleep(5)
            pass
        for track in tracks:
            if track_id in track['SPOTIFY']:
                matched_list.append(playlist)
    if len(matched_list) > 0:
        print("Track found in the following playlist(s):")
        for item in matched_list:
            name = sp.playlist(playlist_id=item, fields='name')['name']
            print(f"{name}: https://open.spotify.com/playlist/{item}")
    return matched_list


if __name__ == '__main__':
    # generate_missing_track_playlist(unmatched_track_ids=unmatched_track_ids)
    # get_playlist()
    # my_tracks = get_my_saved_tracks()
    tmp = fetch_playlist_tracks()
    a = playlists_containing_track(track_id=input('Enter Spotify track ID: '))
    print("K")
