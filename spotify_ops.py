import spotipy
import tqdm
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint
from datetime import datetime
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

    if loops%100 == 0:
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
        playlist_list = sp.current_user_playlists(limit=22)
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
                results_raw += [ {'track': item['track']} ]
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

    if loops%10 == 0:
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
    # unmatched_track_ids = ['471eQ7hcJ7JdGY1NzMmUeg', '3NLrRZoMF0Lx6zTlYqeIo4', '08mG3Y1vljYA6bvDt4Wqkj', '2zYzyRzz6pRmhPzyfMEC8s', '0nsPuwB1QB3SVqpD09UP65', '3Gbyl3XZVeEcnFPiiPR09n', '2o4AknH1hXnleCRW2rH45w', '3UULkHdmLDqBDPmBYltoRE', '7fwycbhYngsgYoeQzidkvH', '75R95k0ICuZBFVEjBauOtt', '2iPTESocncak2Q45oXzKOG', '1Hy0m0aaG67ttQZoytmKd8', '0faXHILILebCGnJBPU6KJJ', '6XimI1O15wpfwUdrCnlrxo', '5pKCDm2fw4k6D6C5Rk646C', '25GC50HslaaruyrKjdu0lP', '7GGJ7uPEFfjhfx2UD3ZNYX', '6eK6eWG03zxQFW8P4OE4Cb', '4Cti8D5eFnO5WQ2DIev9ZI', '326CApbERCzytu8gmUC3Hb', '67OWW2AK0Q1FqBatxyt1s5', '40rvBMQizxkIqnjPdEWY1v', '0COqiPhxzoWICwFCS4eZcp', '3UygY7qW2cvG9Llkay6i1i', '0RF1gbstmvYLLM7Emjxezx', '48pyoRmHoUrSXvlBo1pDEV', '6ndmKwWqMozN2tcZqzCX4K', '6kLSBhzEinnul2SlZVrajD', '36nnDyLNwWGEzqAO8UnZVy', '48NOZRemjwadg6Dwc343hJ', '00ioFqMaPYKk3WbFkn1bvW', '1tBZnhDT8xbgJTs43FiqrD', '05c0LG7DakbvX0gYbBHjPP', '79CATxWpb9uezVeOIazKgs', '07BuyVse8pYAWd9DXD7B2D', '2r7Z355i8dUjhhLsHoH852', '3PbsDnKdrZY0ttX7VE9s5R', '13FYgwCmQy7WyDdLOZgK1y', '1eTdTVIxLlhHwwA50vEzZa', '2302lUwfZ4S4dVyPOCDFnQ', '3ZjnFYlal0fXN6t61wdxhl', '491FFHeud9a0KXZ66QunVn', '00nh13cwyWgGnBkW1aapBO', '5nekfiTN45vlxG0eNJQQye', '2kMjk14RmYyYhhSbipoa9U', '0Kt9sF46S7DFKrQOsXqidV', '4zXvB4MoQD8onk0NCZbeHG', '1EFddFVisHbqCHah6oBlhD', '27tX58NOpv1YKQ0abW7EPy', '1wp1aHirvZihTdrtdFuFv0', '3le4ECmJTUNXYLsGjQYSXi', '1tbjeelOKIjolYNUNnPMAD', '506YO37JuV40cnjeVuwlGD', '4s0O3I5ZpVYfbuZKvNVfRD', '0uctKVLlfFjhYRnJaDaYXM', '3kQxXX13AwkO8Q6qCq2Vv2', '2jGnX8siLIPgKwzqnRpSTD', '1GIofMbTz83fXqNrEuf4bA', '70bK6I56l6TLQmThRhAgfC', '5W8YXBz9MTIDyrpYaCg2Ky', '4oJ4XZwQA2cLMBnRtYSSIb', '4nrWU5PRlFJubLjahofpOU', '1UZvu6rqSIDDfPeJCN5mbz', '53PCsZ23I1bG1NSFFuUYuX', '6FlCPO7Z0QGgwtIL8ocZzY', '3asFGFY3uLjMDmML1p0tYm', '4iLRzDTNc3NbTyQ0w5cAOd', '7cITfGsdjGaTP0b5oiLL0z', '1aDLUzCyYpRXgrjwUWzV2X', '714Lw0m2SmCEhKSPw0Dn8J', '51SHHWOEjxJrEp07SNxow6', '5d9MTgwOIsiGObIv783pgu', '1xJzbzp1WnkVmCkkC5RxEE', '7JJ22vCP45tMhZnAH4Sp1e', '3RptaQ5Xb8WvtpItZ2f9Hi', '6UUhrj3mUGuwjOwg7iw0to', '6Y7vgyXBoedIKgvmZSYXMw', '1ecmyd0EYLAeY5IMPJjGde', '4kG8ckeo4wKsHx4Xk988GE', '4Cvscvb1bbHSsY8lwmSwIQ', '2O0CwwL8CtVH43lJwogt5u', '0vmMXqF1EeLAbgCHGjspdL', '16HleuQoAea2cHLBo2q6Wv', '2wf6TozoLQ1uS2FI7846PA', '2fiqSq32Cy0sEt8ifGenvf', '3J3hQQJ8whGI2zfZXLn7pP', '2cV8T94DdE418bRHMBiJZU', '0Nk2dSrlFJ7FNI0BcK2XAv', '0IbXmxZHkwATLzFG2XQF7r', '5pux00MCk0Qmx54GuLfMfS', '5K9r01YyCQxTOrDSLYwdhS', '6sxtXvoNeOnavXqlIceWch', '2aksJcRQTO5VKqQh1tr3fO', '1Eo7UubnwUOnFymYSc9UyT', '0xBgkHSAhbqxTevZBSPfu6', '6fI7m8uBO8g6m1aaZCayDm', '0AfIsqZ4gTUg9CwwW2jLeK', '68pN2UQYhwQgPy7VrCFKuV', '2DlHlPMa4M17kufBvI2lEN', '4e9eGQYsOiBcftrWXwsVco', '0snQkGI5qnAmohLE7jTsTn', '0GLyqTysS0DFoeKjURtB8s', '6DyywdbmTzlmXBzG9ym7Rt', '75LMfcxCiStv0HewTgCmlx', '6Po2A4lsnVu0GrQ8Dy1nme', '5YOLLCc8sO6PA1B7hlWxMO', '7yuWHdSLrknIYMgbkdmPOS', '4AQ4tIKGLXeBQQsybOKTmv', '6TfBA04WJ3X1d1wXhaCFVT', '4wzjNqjKAKDU82e8uMhzmr', '2Guz1b911CbpG8L92cnglI', '0s1PsjRpN9v3gveUOM6Iux', '0lP4HYLmvowOKdsQ7CVkuq', '5PRx9Px43HHZrzWVAfsGv0', '01v7kv0RTVaX4Vs8GcOGOP', '3HE50TVRquwXe9yv2HFoNL', '5PZ2cqh9Yem2g6cTSOLllz', '0M955bMOoilikPXwKLYpoi', '6OMO6WdRhSfjMPAiPT94wH', '5yDJpu0xh0d1w13gXaE3lS', '2xVuumAfdJpWCqqYZbTI1Q', '272gXQutAYxMC01grHHgET', '4BreyjJu4w5EUhTKPIQymq', '4YPhn26bIFm2KUkL1VLzQG', '3TEwbiC0GhIRStn3Eabtu7', '0gZp88SA5OcujHLDGkxtI3', '1rFAG22RkvaM6BlpWQoZ47']
    # generate_missing_track_playlist(unmatched_track_ids=unmatched_track_ids)
    # get_playlist()
    my_tracks = get_my_saved_tracks()
    print("K")
