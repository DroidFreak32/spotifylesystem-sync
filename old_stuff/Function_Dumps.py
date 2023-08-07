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