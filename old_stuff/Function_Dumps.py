@DeprecationWarning
# db_ops
def search_track_in_db_nonfuzz(track_metadata=None, album_artist=None):
    """
    Scans the DB for a given spotify track and returns a match or an empty list.
        - First perform a case-insensitive match of the AlbumArtist
        - Match the title of track
        - Match the album if title matches to avoid duplicate matches!
            - TODO: Separate logging for such tracks
    :param album_artist:
    :param track_metadata: A spotify track
    :return: Matched item's PATH & STREAMHASH from database.
    """
    result = []
    spotify_title = deepcopy(track_metadata['TITLE'].casefold())
    spotify_album = deepcopy(track_metadata['ALBUM'].casefold())

    for row in album_artist.tracks:
        db_title = deepcopy(row.TITLE.casefold())

        db_album = deepcopy(row.ALBUM.casefold())

        if re.search(rf"\b{re.escape(db_title)}\b", spotify_title) is not None \
                or is_title_in_alt_title(db_row=row, track_metadata=track_metadata) \
                or spotify_title == db_title:
            # For ex "The Diary of Jane" is in "The Diary of Jane - Single Version" so match such cases too.

            if is_item_in_db_column(row.blackTITLE, track_metadata['TITLE']):
                # This track is probably another edition, i.e. Acoustic Version
                # If subsequent iterations do not get this track then it will be a part of unmatched list.
                continue

            if db_title != spotify_title and not is_title_in_alt_title(db_row=row, track_metadata=track_metadata):
                print(f"\nSpotify URL:"
                      f"\n{track_metadata['SPOTIFY']}"
                      f"\nSpotify / DB Title:"
                      f"\n{bcolors.OKBLUE}"
                      f"{track_metadata['TITLE']}{bcolors.ENDC} / {bcolors.OKCYAN}{row.TITLE}"
                      f"{bcolors.ENDC}"
                      f"\n\nPATH {row.PATH}"
                      f"\n\nAre these the same?")
                answer = input("Y/N/Q: ")
                if answer == 'Y' or answer == 'y':
                    print(f"\n*** Ignoring Title ***")
                    add_to_alt_title(db_row=row, track_metadata=track_metadata)
                    spotify_title = db_title
                elif answer == 'q' or answer == 'Q':
                    return 999
                elif answer == 'n' or answer == 'N':
                    add_to_black_title(
                        db_row=row, track_metadata=track_metadata)
                else:
                    continue

            if db_title == spotify_title or is_title_in_alt_title(db_row=row, track_metadata=track_metadata):
                if is_item_in_db_column(row.ALBUM, track_metadata['ALBUM']) \
                        or is_album_in_alt_album(db_row=row, track_metadata=track_metadata):
                    result.append({
                        'ALBUMARTIST': album_artist.ALBUMARTIST,
                        'PATH': liststr_to_list(row.PATH),
                        'STREAMHASH': row.STREAMHASH
                    })
                else:
                    if is_item_in_db_column(row.blackALBUM, track_metadata['ALBUM']):
                        # This track belongs to another existing album in the DB or we do not have it.
                        # If subsequent iterations do not get this track then it will be a part of unmatched list.
                        continue

                    print(f"\nSpotify URL:"
                          f"\n{track_metadata['SPOTIFY']}"
                          f"\nSpotify / DB Album:"
                          f"\n{bcolors.OKBLUE}"
                          f"{track_metadata['ALBUM']}{bcolors.ENDC} / {bcolors.OKCYAN}{row.ALBUM}"
                          f"{bcolors.ENDC}"
                          f"\n\nPATH {row.PATH}"
                          f"\nAre these the same?")
                    answer = input("Y/N/A (All Album)/Q: ")

                    if answer == 'n' or answer == 'N':
                        add_to_black_album(row, track_metadata)
                        continue

                    if answer == 'Y' or answer == 'y' or answer == 'A':
                        if answer == 'A':
                            query = Music.select().where(
                                (Music.ALBUMARTIST == row.ALBUMARTIST) & (Music.ALBUM == row.ALBUM))
                            for row2 in query:
                                add_to_alt_album(row2, track_metadata)
                        else:
                            add_to_alt_album(row, track_metadata)
                            result.append({
                                'ALBUMARTIST': album_artist.ALBUMARTIST,
                                'PATH': liststr_to_list(row.PATH),
                                'STREAMHASH': row.STREAMHASH
                            })
                            continue
                    elif answer == 'q' or answer == 'Q':
                        return 999
                    else:
                        continue
                # if spotify_album_artist not in result.keys():
                #     result[spotify_album_artist] = []
                #
                # result[spotify_album_artist].append({
                #     'PATH': str_to_list(row.PATH),
                #     'STREAMHASH': row.STREAMHASH
                # })
    return result


def fast_search_track_in_db(track_metadata=None, album_artist=None):
    """
    Scans the DB for a given spotify track and returns a match or an empty list.
        - First perform a case-insensitive match of the AlbumArtist
        - Match the title of track
        - Match the album if title matches to avoid duplicate matches!
            - TODO: Separate logging for such tracks
    :param album_artist:
    :param track_metadata: A spotify track
    :return: Matched item's PATH & STREAMHASH from database.
    """

    album_artist_tracks = None
    unique_tids = None
    result = []
    spotify_title = deepcopy(track_metadata['TITLE'].casefold())
    spotify_album = deepcopy(track_metadata['ALBUM'].casefold())
    spotify_tid = deepcopy(track_metadata['SPOTIFY_TID'])
    spotify_linked_tid = deepcopy(track_metadata['SPOTIFY_LINKED_TID'])
    db_track_contains_tid = False

    stage = 0

    album_artist_tracks = Music.select().where(
        (Music.SPOTIFY_TID.contains(spotify_tid)) | (Music.SPOTIFY_TID.contains(spotify_linked_tid))
    )

    if len(album_artist_tracks) >= 1:
        db_track_contains_tid = True

    for row in album_artist_tracks:
        # Reset these flags in each iteration
        bypass_title = False
        bypass_album = False

        db_title = deepcopy(row.TITLE.casefold())

        db_album = deepcopy(row.ALBUM.casefold())

        ##########################
        # Album Matching section #
        ##########################
        if True or bypass_title or db_title == spotify_title or \
                is_title_in_alt_title(db_row=row, track_metadata=track_metadata):

            track_matches_spot_album, path_index = is_item_in_db_column_with_index(db_album,
                                                                                   spotify_album)

            # We cannot use fuzz as we want to ensure the album is exactly the same or prompt the user!
            if True or track_matches_spot_album \
                    or is_album_in_alt_album(db_row=row, track_metadata=track_metadata):
                """
                TODO: If there are multiple paths, use the path index corresponding to the matching Album index.
                For ex, spotify's "My Propeller" belongs to DB Albums [My Propeller, Humbug]
                So return the path corresponding to the matched album.
                Since they are the same track, it *probably* won't be queried again after its matched.
                """
                if path_index is not None:
                    # ~Why a list? User might say yes to a track with multiple paths manually~
                    # TAG: cd213e2f
                    track_path = [liststr_to_list(row.PATH)[path_index]]
                else:
                    track_path = liststr_to_list(row.PATH)

                if db_track_contains_tid:
                    db_tids = liststr_to_list(row.SPOTIFY_TID)
                    db_tids.sort()
                    unique_tids = sorted(
                        set([spotify_tid, spotify_linked_tid] + db_tids)
                    )
                    if len(unique_tids) == len(db_tids):
                        skip_db_update = True
                        # PROFILE THIS!! MAY NOT BE NEEDED
                        if db_tids != unique_tids:
                            pass

                result.append({
                    'ALBUMARTIST': album_artist.ALBUMARTIST,
                    'PATH': track_path,
                    'ARTIST': liststr_to_list(row.ARTIST),
                    'SPOTIFY_TID': unique_tids,
                    'STREAMHASH': row.STREAMHASH,
                })


    """
    If there's multiple matches, there is a chance that we are searching for a compilation album like
    "The Metallica Blacklist" that contains tracks from various artists under the same Album Artist.
    In these cases, try to see if the if the artists in the DB match spotify metadata.
     - If there's a list of artists for a track in the DB, this list should be a subset of
        Spotify track metadata as well. (And Vice Versa)
     - If it's a single artist, it should match the first artist in Spotify track metadata.
     TODO: There may be false positives!
    """
    if len(result) > 1:
        trimmed_result = []
        track_metadata_artist = [x.lower() for x in track_metadata['ARTIST']]
        for item in result:
            if isinstance(item['ARTIST'], list):

                # First Make the DB artist list case-insensitive!
                item['ARTIST'] = [x.lower() for x in item['ARTIST']]

                if set(item['ARTIST']).issubset(track_metadata_artist) or \
                        set(track_metadata_artist).issubset(item['ARTIST']):

                    trimmed_result.append(item)

            else:
                if item['ARTIST'].lower() in track_metadata_artist:
                    trimmed_result.append(item)
        return trimmed_result

    elif len(result) == 0:
        stage += 1
    else:
        return result

    return result


def fast_generate_local_playlist(all_saved_tracks=False, skip_playlist_generation=False):

    """
    TODO: Instead of scanning each track, merge the AlbumArtist and just have 1 lookup per AA in DB
    TODO: Parallelize DB searching by adding a flag to bypass any user prompts and just store all the SUCCESS results
            then strip these tracks and redo the classic brute-force searching which then asks for prompts.
            For large number of songs of the artist, this method could be used:
    album_artist = AlbumArtist.get(...)
    fast_result = a_pool.starmap(search_track_in_db, zip(spotify_playlist_tracks_merged['Arctic Monkeys'], repeat(album_artist)))
    """
    # Flags to quit generating playlists.
    skip_generation_and_save = False
    abort_abort = False

    # Copy DB in memory to avoid mistakes being reflected into the main DB.
    master = CSqliteExtDatabase(db_path)
    master.backup(db)
    if not all_saved_tracks:
        spotify_playlist_name, spotify_playlist_tracks = spotify_ops.fetch_playlist_tracks(owner_only=True)
    else:
        # spotify_playlist_name, spotify_playlist_tracks = spotify_ops.get_my_saved_tracks()
        # with open("allmytracks.json", "w") as jsonfile:
        #     jsonfile.write(json.dumps(deepcopy(spotify_playlist_tracks), indent=4, sort_keys=False))
        with open('allmytracks.json', 'r') as j:
            spotify_playlist_tracks = json.loads(j.read())
        spotify_playlist_name = 'RuMAN'
    spotify_playlist_track_total = len(spotify_playlist_tracks)
    matched_list = []
    matched_paths = []
    unmatched_track_ids = []
    unmatched_list = []
    spotify_playlist_tracks_merged = list2dictmerge(
        deepcopy(spotify_playlist_tracks))

    offset = 0
    for spotify_album_artist in spotify_playlist_tracks_merged.keys():
        try:
            album_artist = AlbumArtist.get(
                AlbumArtist.ALBUMARTIST == spotify_album_artist)
        except DoesNotExist:
            try:
                # Maybe some casing is different
                album_artist = AlbumArtist.get(
                    AlbumArtist.ALBUMARTIST == spotify_album_artist.casefold())
            except DoesNotExist:
                # Add all tracks of this artist to unmatched tracks and increase offset accordingly
                skipped_tracks = []
                for track in spotify_playlist_tracks_merged[spotify_album_artist]:
                    skipped_tracks.append(
                        {'ALBUMARTIST': spotify_album_artist} | track
                    )

                #     if track['SPOTIFY_TID'] != track['SPOTIFY_LINKED_TID']:
                #         unmatched_track_ids.append(spotify_ops.return_saved_tid(
                #             [track['SPOTIFY_TID'], track['SPOTIFY_LINKED_TID']]
                #         ))
                #     else:
                #         unmatched_track_ids.append(track['SPOTIFY_TID'])
                #
                # unmatched_list += skipped_tracks
                offset += len(skipped_tracks)
                continue

        skip_generation_and_save = False
        abort_abort = False
        offset += 1
        print(
            f"Querying DB for tracks: {offset} / {spotify_playlist_track_total}", end="\r")

        # result = \
        #     search_track_in_db(track_metadata=playlist_track, album_artist=album_artist)
        #
        a_pool = multiprocessing.Pool(2)
        results = a_pool.starmap(fast_search_track_in_db, zip(spotify_playlist_tracks_merged[spotify_album_artist], repeat(album_artist)))

        # BUG: This seems to SEGSEV,maybe DB does not like so many parallel queries
        pass
        track_index = -1
        for result in results:
            track_index += 1

            if result == 9:
                skip_generation_and_save = True
                break
            elif result == 99:
                abort_abort = True
                break
            if len(result) > 1:
                print(
                    f"{bcolors.FAIL}Multiple Matches found: {result}{bcolors.ENDC}")
                # TODO: Ask user for correct match by checking playlist_track['SPOTIFY']
                continue
            elif len(result) == 0:
                unmatched_track = {'ALBUMARTIST': spotify_album_artist} | spotify_playlist_tracks_merged[spotify_album_artist][track_index]
                unmatched_list.append(unmatched_track)
                if unmatched_track['SPOTIFY_TID'] != unmatched_track['SPOTIFY_LINKED_TID']:
                    unmatched_track_ids.append(spotify_ops.return_saved_tid(
                        [unmatched_track['SPOTIFY_TID'], unmatched_track['SPOTIFY_LINKED_TID']]
                    ))
                else:
                    unmatched_track_ids.append(unmatched_track['SPOTIFY_TID'])
                # print(f"No result found for {playlist_track['ALBUMARTIST']} - {playlist_track['TITLE']}")
                continue
            matched_list += result
            if isinstance(liststr_to_list(result[0]['PATH']), list):
                # Use the 1st PATH. TODO: Make this more accurate by checking Album
                # TAG: cd213e2f
                result[0]['PATH'] = result[0]['PATH'][0]
            matched_paths.append(result[0]['PATH'])
    if abort_abort:
        print(f"{bcolors.WARNING}Aborting!{bcolors.ENDC}")
        return
    elif skip_generation_and_save:
        exit()

    # for item in matched_list:
    #     update_trackid_in_db(spotify_tid=item['SPOTIFY_TID'], streamhash=item['STREAMHASH'])
    unmatched_dict = list2dictmerge(deepcopy(unmatched_list))
    matched_dict = list2dictmerge(deepcopy(matched_list))
    print(f"\n{len(matched_list)}/{spotify_playlist_track_total} tracks Matched. ")

    if not skip_playlist_generation:
        if input("Do you want to generate an m3u file for the matched songs?\nY/N: ")[0].casefold() == 'y':
            generate_m3u(playlist_name=spotify_playlist_name, track_paths=matched_paths)
        if len(unmatched_track_ids) > 0:
            if input("Do you want to generate a new spotify playlist "
                     "for the UNMATCHED songs?\nY/N: ")[0].casefold() == 'y':
                spotify_ops.generate_playlist_from_tracks(track_ids=unmatched_track_ids,
                                                          playlist_name=spotify_playlist_name)

    with open("unmatched.json", "w") as jsonfile:
        encoded_json = json.dumps(unmatched_dict, indent=4, sort_keys=True, ensure_ascii=False)
        jsonfile.write(encoded_json)
    with open("matched.json", "w") as jsonfile:
        encoded_json = json.dumps(matched_dict, indent=4, sort_keys=True, ensure_ascii=False)
        jsonfile.write(encoded_json)


# spotify_ops
@DeprecationWarning
def get_playlist(playlist_id=None, list_only=False):
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
        # playlist = sp.playlist(selected_playlist_id, fields='id, name, tracks.total, owner.id')
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