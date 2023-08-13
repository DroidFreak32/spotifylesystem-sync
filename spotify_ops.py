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
    _, playlist_tracks = fetch_playlist_tracks(playlist_id=playlist_id)
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


def get_proper_albumartist(artist_list=None, warning=False):
    """
    Multiple Album artists should not exist. Artist tag should be used for featured artists.
    :param artist_list:
    :return: 1st name in AlbumArtists
    """
    if len(artist_list) > 1 and warning:
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
        # Initialize
        track = dict()
        track['ALBUMARTIST'] = get_proper_albumartist(item['track']['album']['artists'])
        track['ALBUM'] = item['track']['album']['name']
        track['TITLE'] = item['track']['name']
        track['ARTIST'] = get_proper_artist(item['track']['artists'])
        track['SPOTIFY'] = item['track']['external_urls']['spotify']
        track['SPOTIFY_TID'] = item['track']['id']
        if 'linked_from' in item['track']:
            track['SPOTIFY_LINKED_TID'] = item['track']['linked_from']['id']
        else:
            # This is to prevent Null exceptions while performing DB Query on this key
            track['SPOTIFY_LINKED_TID'] = item['track']['id']

        # track['SPOTIFY_TID'] = item['track']['id']
        if track['ALBUMARTIST'] == 'Various Artists':
            track['ALBUMARTIST'] = get_proper_albumartist(item['track']['artists'])
        cleaned_playlist.append(track)
    return cleaned_playlist


############################################
# Externally callable functions start here #
############################################

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
    """
Prompts user to select a specific playlist from their saved playlists
    @param user_id: User whose playlists should be listed, set to the current authenticated API user if None
    @param owner_only: If True, only playlists created by user_id will be selected
    @return: The ID of selected Playlist
    """
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
        # Ensures each column does not take more than the number of characters specified below
        print("{:<3}) ID: {:<22} Tracks:{:<5} By:{:<15} Name: {:<22}"
              .format(index, key, value[1], value[2][:15], value[0][:22] + '..'))
        index += 1

    answer = input("Enter the playlist ID: ")

    # If user chooses the enter the number, translate it to the list's index
    if answer.isnumeric():
        playlist_id = list(playlists.keys())[int(answer) - 1]
    else:
        playlist_id = answer
    return playlist_id


def fetch_playlist_tracks(user_id=None, playlist_id=None, owner_only=False):
    """
Finds all tracks from a given playlist ID

    @param user_id: User whose playlists should be listed
    @param playlist_id: If not specified, call select_user_playlist to prompt user for a specific ID
    @param owner_only: If True, only playlists created by user_id will be selected
    @return: Touple of the playlist's Name and track list
    """
    if user_id is None:
        user_id = sp.me()['id']
    if playlist_id is None:
        playlist_id = select_user_playlist(user_id=user_id, owner_only=owner_only)

    playlist = sp.playlist(playlist_id=playlist_id)
    playlist_name = playlist['name']
    playlist_tracktotal = playlist['tracks']['total']

    offset = 0
    loops = int(playlist_tracktotal / 100) + 1

    if loops % 100 == 0:
        loops -= 1

    full_playlist_raw = []
    for i in range(loops):
        # BUG: Local tracks crash this method, capture them.
        # Use Market parameter to retrieve linked track IDs
        # https://developer.spotify.com/documentation/web-api/concepts/track-relinking
        playlist_raw = sp.playlist_items(playlist_id=playlist_id, offset=offset, market="IN",
                                         fields='items.track.album.artists.name,'
                                                'items.track.album.name,'
                                                'items.track.artists,'
                                                'items.track.id,'
                                                'items.track.linked_from.id,'
                                                'items.track.is_local,'
                                                'items.track.name,'
                                                'items.track.external_urls.spotify',
                                         additional_types=['track'])['items']
        full_playlist_raw += playlist_raw
        offset += 100
        # print(f"Retrieved {offset} / {playlist_tracktotal} tracks from playlist.", end="\r", flush=True)

    playlist_tracks = cleanup_playlist(full_playlist_raw)

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


def generate_playlist_from_tracks(track_ids=None, playlist_name=None, playlist_id=None):
    if track_ids is None:
        track_ids = []
    total_tracks = len(track_ids)
    if total_tracks < 1:
        return

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
        current_batch_of_tracks = track_ids[offset:offset + 10]
        sp.playlist_add_items(playlist_id=playlist_id, items=current_batch_of_tracks)
        offset += 10

    missing_playlist_items = get_missing_playlist_items_from_trackids(
        playlist_id=playlist_id, track_ids=track_ids)

    if missing_playlist_items is not None:
        print(f"Few Tracks Missing")
        generate_playlist_from_tracks(
            track_ids=missing_playlist_items, playlist_name=playlist_name, playlist_id=playlist_id)
    print(f"Playlist: {playlist_name} created!")

    return None


def playlists_containing_tracks(track_ids=None, playlist_list=None, owner_only=True):
    """
    Returns a list of playlist that contains a particular track ID
    @param owner_only: Only search playlists where current user is the owner
    @param track_ids: List of IDs of the tracks from spotify's URL.
    Ex: URL: https://open.spotify.com/track/0lkQOB949M2gLyut86aJ1b?si=5b3b7ecd2ad44a2a
        track_id: ['0lkQOB949M2gLyut86aJ1b']
    @param playlist_list: A list of spotify Playlist IDs to search, defaults to all saved playlists.
    @return: A list of user's saved spotify playlists' IDs that have the track.
    """
    matched_list = {}
    if track_ids is None:
        track_ids = [input("Enter Spotify track's ID")]
    if playlist_list is None:
        playlist_list = fetch_user_playlists(owner_only=owner_only, ids_only=True)
    cooldown = 0

    # Initialize matched list
    for track_id in track_ids:
        matched_list[track_id] = []

    for playlist in playlist_list:
        cooldown += 1
        playlist_name, tracks = fetch_playlist_tracks(playlist_id=playlist)

        # Cooldown every 5 iterations to avoid TOO many API requests
        if not (cooldown % 5):
            time.sleep(5)
            pass
        for track_id in track_ids:
            for track in tracks:
                if track_id in track['SPOTIFY']:
                    matched_list[track_id].append(playlist)
            # if len(matched_list[track_id]) == 0:
            #     del matched_list[track_id]
            #     print(f"Track with ID {track_id} not found in any saved playlist")

    for requested_track, playlists_containing_track in matched_list.items():
        track_name = sp.track(requested_track)["name"]
        print(f"Track {track_name} with ID {requested_track} found in the following playlist(s):")
        for item in playlists_containing_track:
            playlist_name = sp.playlist(playlist_id=item, fields='name')['name']
            print(f"{playlist_name}: https://open.spotify.com/playlist/{item}")

    # if len(matched_list) > 0:
    #     print("Track found in the following playlist(s):")
    #     for item in matched_list:
    #         name = sp.playlist(playlist_id=item, fields='name')['name']
    #         print(f"{name}: https://open.spotify.com/playlist/{item}")
    return matched_list


def find_playlists_containing_tracks():

    print('Enter Spotify track IDs to search, hit enter twice to Finish:')

    tracks = []
    prompt = "-> "
    line = input(prompt)
    while line:
        tracks.append(line)
        line = input(prompt)

    a = playlists_containing_tracks(track_ids=tracks)


def generate_unsaved_track_playlists(owner_only=True, all_playlists=False, merged=False):

    playlist_counter = 0
    playlists_count = 0
    unsaved_tracks = []
    unsaved_indices = []

    if all_playlists:
        playlist_ids = fetch_user_playlists(owner_only=owner_only, ids_only=True)
        playlists_count = len(playlist_ids)
    else:
        print(f"Select the playlist to search")
        playlist_ids = [select_user_playlist(owner_only=owner_only)]

    for playlist_id in playlist_ids:
        max_tracks = 50

        # Skip resetting unsaved_tracks if we want to merge all unsaved tracks from all playlist at once
        if not merged:
            unsaved_tracks = []
            unsaved_indices = []

        playlist_name, playlist_tracks = fetch_playlist_tracks(playlist_id=playlist_id)

        if all_playlists:
            playlist_counter += 1
            print(f"Scanning playlist {playlist_counter}/{playlists_count}: {playlist_name} ..", end="\r")

        tracklist = []
        for track in playlist_tracks:
            # Some tracks are Linked https://developer.spotify.com/documentation/web-api/concepts/track-relinking
            # So include both to prevent false negatives where a track is added in the unsaved tracks playlist
            # when in fact an alternate ID of the same track is actually present in Liked Songs.
            # Later we will check both IDs in 2 stages to get a final list of Saved/Unsaved tracks
            tracklist.append((track['SPOTIFY_TID'], track['SPOTIFY_LINKED_TID']))

        offset = 0
        tracklist_saved_status = []

        quotient = int(len(tracklist) / max_tracks)
        if len(tracklist) % max_tracks == 0:
            loops = quotient
        else:
            loops = quotient + 1

        for i in range(loops):
            tracklist_tids = []
            tracklist_linked_tids = []

            # Using offset to avoid API limit
            for j in tracklist[offset:offset+max_tracks]:
                # Stage 1, TID
                tracklist_tids.append(j[0])
                # Stage 2, Linked TID
                tracklist_linked_tids.append(j[1])

            if tracklist_tids == tracklist_linked_tids:
                # Both TIDs are the same so skip redundant API requests
                stage_1 = stage_2 = sp.current_user_saved_tracks_contains(tracklist_tids)
            else:
                # Different TIDs detected so get 2 lists checking both IDs
                stage_1 = sp.current_user_saved_tracks_contains(tracklist_tids)
                stage_2 = sp.current_user_saved_tracks_contains(tracklist_linked_tids)

            # Perform bitwise OR on both stages to get the true list of unsaved Tracks
            # https://stackoverflow.com/a/47419515
            tracklist_saved_status += [x or y for (x, y) in zip(stage_1, stage_2)]
            offset += max_tracks
            # To avoid API limits
            time.sleep(0.5)

        # Identify the index of tracks that are genuinely not saved by getting the position of !True items
        # https://stackoverflow.com/questions/21448225/getting-indices-of-true-values-in-a-boolean-list
        unsaved_indices = [i for i, s in enumerate(tracklist_saved_status) if not s]
        for i in unsaved_indices:
            unsaved_tracks += sorted(
                {tracklist[i][0], tracklist[i][1]}
            )
        pass

        if not merged:
            generate_playlist_from_tracks(track_ids=unsaved_tracks, playlist_name=playlist_name)

    if merged:
        generate_playlist_from_tracks(track_ids=unsaved_tracks, playlist_name="MEGA_UNSAVED")


def delete_tracks_from_playlist(owner_only=True):
    max_tracks = 50
    unsaved_tracks = []
    unsaved_indices = []

    if input(f"Enter Y to delete from playlists not owned by you:").casefold() == 'y':
        owner_only = False
    print(f"Select the \"Eraser\" playlist that contains tracks to be deleted")
    src_playlist_id = select_user_playlist(owner_only=True)

    print(f"Select the \"Target\" playlist whose tracks will be deleted")
    dst_playlist_id = select_user_playlist(owner_only=owner_only)

    src_playlist_name, src_playlist_tracks = fetch_playlist_tracks(playlist_id=src_playlist_id)

    tracklist = []
    for track in src_playlist_tracks:
        tracklist += sorted({track['SPOTIFY_TID'], track['SPOTIFY_LINKED_TID']})

    offset = 0
    quotient = int(len(tracklist) / max_tracks)
    if len(tracklist) % max_tracks == 0:
        loops = quotient
    else:
        loops = quotient + 1

    for i in range(loops):
        sp.playlist_remove_all_occurrences_of_items(
            playlist_id=dst_playlist_id, items=tracklist[offset:offset+max_tracks]
        )
        offset += max_tracks


def return_saved_tid(tids=None):

    if tids is None:
        tids = []
    results = sp.current_user_saved_tracks_contains(tids)
    return tids[0] if results[0] else tids[1]


if __name__ == '__main__':
    # generate_missing_track_playlist(unmatched_track_ids=unmatched_track_ids)
    # get_playlist()
    # my_tracks = get_my_saved_tracks()
    # tmp = fetch_playlist_tracks()
    # delete_tracks_from_playlist()
    # generate_unsaved_track_playlists(all_playlists=True, merged=True)
    print("K")
