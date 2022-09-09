import os
import re
from asyncio import subprocess
from copy import deepcopy
from pathlib import Path
from pprint import pprint

from fuzzywuzzy import fuzz
from peewee import BlobField
from peewee import CharField
from peewee import DoesNotExist
from peewee import ForeignKeyField
from peewee import IntegrityError
from peewee import Model
from peewee import TextField
from playhouse.sqlite_ext import CSqliteExtDatabase

import spotify_ops
from common import bcolors, fetch_metadata_in_background, generate_m3u, generate_metadata, get_last_flac_mtime, \
    list2dictmerge, music_root_dir, \
    db_path, db_mtime_marker
from common import str_to_list, find_flacs

db = CSqliteExtDatabase(":memory:")


class BaseModel(Model):
    class Meta:
        database = db


class AlbumArtist(BaseModel):
    ALBUMARTIST = TextField(index=True)


class Music(BaseModel):
    ALBUMARTIST = ForeignKeyField(AlbumArtist, backref="tracks")
    ARTIST = TextField(index=True)

    ALBUM = TextField(index=True)
    # List of alternate album names, usually from spotify
    altALBUM = TextField(null=True)
    # List of albums that is not present in the DB but the track exists in another Album
    blackALBUM = TextField(null=True, unindexed=True)

    TITLE = TextField(index=True)
    altTITLE = TextField(null=True)
    blackTITLE = TextField(null=True, unindexed=True)

    LYRICS = BlobField(unindexed=True, null=True)
    STREAMHASH = CharField(max_length=32, unique=True)
    PATH = TextField(unindexed=True)


def is_item_in_db_column(db_tag=None, track_tag=None):
    """
    Checks if a particular tag is present on a given db column
    Handles cases where column may contain a list.
    """
    if db_tag is None:
        return False
    if isinstance(str_to_list(db_tag), list):
        for tag in str_to_list(db_tag):
            if tag.casefold() == track_tag.casefold():
                return True
    if db_tag.casefold() == track_tag.casefold():
        return True
    return False


def is_album_in_alt_album(db_row, track_metadata):
    """
    Separate this as it is always a list
    """
    if db_row.altALBUM is not None:
        for item in str_to_list(db_row.altALBUM):
            if item.casefold() == track_metadata['ALBUM'].casefold():
                return True

    return False


def is_title_in_alt_title(db_row, track_metadata):
    """
    Separate this as it is always a list
    """
    if db_row.altTITLE is not None:
        for item in str_to_list(db_row.altTITLE):
            if item.casefold() == track_metadata['TITLE'].casefold():
                return True

    return False


def add_to_alt_album(db_row, track_metadata):
    """
    Function to add to a whitelist column.
    """
    altALBUM_to_add = str_to_list(db_row.altALBUM)
    # TODO: This is just a POC. add more functions to get existing values/lists before adding
    if isinstance(altALBUM_to_add, list):
        altALBUM_to_add.append(track_metadata['ALBUM'])
    else:
        altALBUM_to_add = [track_metadata['ALBUM']]

    print(
        f"\n{bcolors.OKGREEN}Adding {altALBUM_to_add} to alt Albums{bcolors.ENDC}\n")
    query = Music.update(altALBUM=altALBUM_to_add).where(
        Music.STREAMHASH == db_row.STREAMHASH)
    query.execute()


def add_to_alt_title(db_row, track_metadata):
    """
    Function to add to a whitelist column.
    """
    altTITLE_to_add = str_to_list(db_row.altTITLE)
    # TODO: This is just a POC. add more functions to get existing values/lists before adding
    if isinstance(altTITLE_to_add, list):
        altTITLE_to_add.append(track_metadata['TITLE'])
    else:
        altTITLE_to_add = [track_metadata['TITLE']]

    print(f"{bcolors.OKGREEN}Adding {altTITLE_to_add} to alt Titles{bcolors.ENDC}\n")
    query = Music.update(altTITLE=altTITLE_to_add).where(
        Music.STREAMHASH == db_row.STREAMHASH)
    query.execute()


def add_to_black_album(db_row, track_metadata):
    blackALBUM_to_add = str_to_list(db_row.blackALBUM)
    # TODO: This is just a POC. add more functions to get existing values/lists before adding
    if isinstance(blackALBUM_to_add, list):
        blackALBUM_to_add.append(track_metadata['ALBUM'])
    else:
        blackALBUM_to_add = [track_metadata['ALBUM']]

    print(
        f"\n{bcolors.HEADER}Adding {blackALBUM_to_add} to blacklist{bcolors.ENDC}\n")
    query = Music.update(blackALBUM=blackALBUM_to_add).where(
        Music.STREAMHASH == db_row.STREAMHASH)
    query.execute()


def add_to_black_title(db_row, track_metadata):
    blackTITLE_to_add = str_to_list(db_row.blackTITLE)
    # TODO: This is just a POC. add more functions to get existing values/lists before adding
    if isinstance(blackTITLE_to_add, list):
        blackTITLE_to_add.append(track_metadata['TITLE'])
    else:
        blackTITLE_to_add = [track_metadata['TITLE']]

    print(
        f"\n{bcolors.HEADER}Adding {blackTITLE_to_add} to blacklist{bcolors.ENDC}\n")
    query = Music.update(blackTITLE=blackTITLE_to_add).where(
        Music.STREAMHASH == db_row.STREAMHASH)
    query.execute()


@DeprecationWarning
def search_track_in_db_nonfuzz(track_metadata=None, album_artist=None):
    """
    Scans the DB for a given spotify track and returns a match or an empty list.
        - First perform a case-insensitive match of the AlbumArtist
        - Match the title of track
        - Match the album if title matches to avoid duplicate matches!
            - TODO: Separate logging for such tracks
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
                      f"\n{bcolors.OKBLUE}{track_metadata['TITLE']}{bcolors.ENDC} / {bcolors.OKCYAN}{row.TITLE}{bcolors.ENDC}"
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
                        'PATH': str_to_list(row.PATH),
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
                          f"\n{bcolors.OKBLUE}{track_metadata['ALBUM']}{bcolors.ENDC} / {bcolors.OKCYAN}{row.ALBUM}{bcolors.ENDC}"
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
                                'PATH': str_to_list(row.PATH),
                                'STREAMHASH': row.STREAMHASH
                            })
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


def search_track_in_db(track_metadata=None, album_artist=None):
    """
    Scans the DB for a given spotify track and returns a match or an empty list.
        - First perform a case-insensitive match of the AlbumArtist
        - Match the title of track
        - Match the album if title matches to avoid duplicate matches!
            - TODO: Separate logging for such tracks
    :param track_metadata: A spotify track
    :return: Matched item's PATH & STREAMHASH from database.
    """
    result = []
    spotify_title = deepcopy(track_metadata['TITLE'].casefold())
    spotify_album = deepcopy(track_metadata['ALBUM'].casefold())

    for row in album_artist.tracks:
        db_title = deepcopy(row.TITLE.casefold())

        db_album = deepcopy(row.ALBUM.casefold())

        if fuzz.ratio(db_title, spotify_title) >= 90 \
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
                      f"\n{bcolors.OKBLUE}{track_metadata['TITLE']}{bcolors.ENDC} / {bcolors.OKCYAN}{row.TITLE}{bcolors.ENDC}"
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
                        'PATH': str_to_list(row.PATH),
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
                          f"\n{bcolors.OKBLUE}{track_metadata['ALBUM']}{bcolors.ENDC} / {bcolors.OKCYAN}{row.ALBUM}{bcolors.ENDC}"
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
                                'PATH': str_to_list(row.PATH),
                                'STREAMHASH': row.STREAMHASH
                            })
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


def dump_to_db(metadata):
    music_db_orm = None
    for album_artists, track_list in metadata.items():
        AlbumArtist.create(ALBUMARTIST=album_artists)
        for track in track_list:
            """
            Get an AlbumArtist object, maybe for backref?? Blind copy pasta
            """
            album_artist = AlbumArtist.get(
                AlbumArtist.ALBUMARTIST == album_artists)
            try:
                music_db_orm = Music.create(ALBUMARTIST=album_artist, ARTIST=track['ARTIST'], ALBUM=track['ALBUM'],
                                            altALBUM=None, blackALBUM=None,
                                            TITLE=track['TITLE'], altTITLE=None, blackTITLE=None,
                                            LYRICS=track['LYRICS'],
                                            STREAMHASH=track['STREAMHASH'],
                                            PATH=track['PATH'])
            except IntegrityError as IE:
                """
                Some music files may belong to multiple albums, for ex. "Self titled" and "Greatest hits"
                So we can just query the existing file and convert the relevant columns to a list of values 
                """
                if music_db_orm is not None:
                    music_db_orm.save()
                print(f"{bcolors.WARNING}Identical Track found!")
                query = Music.select().where(Music.STREAMHASH ==
                                             track["STREAMHASH"]).dicts()
                multi_path = []
                multi_album = []
                for row in query:
                    """
                    Either append to existing Albums & Paths or convert to a list of Albums and Paths.
                    Also handle *-copy.flac files which ONLY have a different PATH
                    """

                    if isinstance(str_to_list(row['PATH']), list):
                        multi_path = str_to_list(row['PATH'])
                        multi_path.append(track['PATH'])
                    else:
                        multi_path.append(row['PATH'])
                        multi_path.append(track['PATH'])
                    if isinstance(str_to_list(row['ALBUM']), list):
                        multi_album = str_to_list(row['ALBUM'])
                        multi_album.append(track['ALBUM'])
                    elif track['ALBUM'] == row['ALBUM']:
                        print(
                            f"{bcolors.WARNING}Is this file a duplicate copy?{bcolors.ENDC}")
                        multi_album = track['ALBUM']
                    else:
                        multi_album.append(row['ALBUM'])
                        multi_album.append(track['ALBUM'])
                    # print(multi_path)
                    query = Music.update(ALBUMARTIST=album_artist, ARTIST=track['ARTIST'], ALBUM=multi_album,
                                         altALBUM=row['altALBUM'], blackALBUM=row['blackALBUM'],
                                         TITLE=track['TITLE'], altTITLE=row['altTITLE'], blackTITLE=row['blackTITLE'],
                                         LYRICS=track['LYRICS'],
                                         PATH=multi_path).where(Music.STREAMHASH == track["STREAMHASH"])
                    query.execute()
                print(
                    f"Previous file: {multi_path[0]}\nCurrent file: {multi_path[1]}{bcolors.ENDC}")

    if music_db_orm is not None:
        music_db_orm.save()


def sync_fs_to_db(force_resync=True, flac_files=find_flacs(music_root_dir), last_flac_mtime=1):
    master = CSqliteExtDatabase(db_path)
    master.backup(db)
    if force_resync:
        last_flac_mtime = get_last_flac_mtime(flac_files)
        db.drop_tables([AlbumArtist, Music])
        db.create_tables([AlbumArtist, Music])

    metadata = generate_metadata(music_root_dir, flac_files)
    answer = input("\nIf there are warnings above, for example - Multiple Album Artist tag in a file " +
                   "\nstop this program and fix them. Else, type F to ignore the warnings and continue.")
    if answer == 'F' or answer == 'f':
        answer = input("Are you really sure you want to ignore the warnings? (Y/N)")
        if answer == 'Y' or answer == 'y':
            dump_to_db(metadata)
            print("METADATA SYNCED")
            db.backup(master)
            master.execute_sql('VACUUM;')
            Path(db_mtime_marker).touch()
            # Write the timestamp  to the file
            command = f"echo {str(last_flac_mtime)} > {db_mtime_marker}"
            subprocess.Popen(command, shell=True)
            os.utime(db_mtime_marker, (last_flac_mtime, last_flac_mtime))
            print(os.path.getmtime(db_mtime_marker))
            return

        # Exit due to warnings
        print("\nExiting!")
        exit(1)


def partial_sync():
    flac_files = find_flacs(music_root_dir)
    new_files = []
    # read the last modified time
    with open(db_mtime_marker) as f:
        db_mtime = float(f.readline().strip())
    last_flac_mtime = get_last_flac_mtime(flac_files)
    for flac_file in flac_files:
        if db_mtime < os.path.getmtime(os.path.join(music_root_dir, flac_file)):
            new_files.append(flac_file)
    print(f"New files:\n_________")
    pprint(new_files)
    input("Press enter to continue..")
    if len(new_files) > 0:
        sync_fs_to_db(force_resync=False, flac_files=new_files,
                      last_flac_mtime=last_flac_mtime)


def generate_local_playlist(all_saved_tracks=False):
    """
    TODO: Instead of scanning each track, merge th AlbumArtist and just have 1 lookup per AA in DB
    """
    global json
    master = CSqliteExtDatabase(db_path)
    master.backup(db)
    if not all_saved_tracks:
        spotify_playlist_name, spotify_playlist_tracks = spotify_ops.get_playlist()
    else:
        # spotify_playlist_name, spotify_playlist_tracks = spotify_ops.get_my_saved_tracks()
        # with open("allmytracks.json", "w") as jsonfile:
        #     jsonfile.write(json.dumps(deepcopy(spotify_playlist_tracks), indent=4, sort_keys=False))

        import json as json
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
            # ** here is for case-insensitive matching
            album_artist = AlbumArtist.get(
                AlbumArtist.ALBUMARTIST ** spotify_album_artist.casefold())
        except DoesNotExist:
            # Add all tracks of this artist to unmatched tracks and increase offset accordingly
            skipped_tracks = []
            for track in spotify_playlist_tracks_merged[spotify_album_artist]:
                skipped_tracks.append(
                    {'ALBUMARTIST': spotify_album_artist} | track)
                unmatched_track_ids.append(track['SPOTIFY'][-22:])
            unmatched_list += skipped_tracks
            offset += len(skipped_tracks)
            continue

        for playlist_track in spotify_playlist_tracks_merged[spotify_album_artist]:
            offset += 1
            print(
                f"Querying DB for tracks: {offset} / {spotify_playlist_track_total}", end="\r")
            result = search_track_in_db(
                track_metadata=playlist_track, album_artist=album_artist)
            if result == 999:
                break
            if len(result) > 1:
                print(
                    f"{bcolors.FAIL}Multiple Matches found: {result}{bcolors.ENDC}")
                # TODO: Ask user for correct match by checking playlist_track['SPOTIFY']
                continue
            elif len(result) == 0:
                unmatched_track = {
                                      'ALBUMARTIST': spotify_album_artist} | playlist_track
                unmatched_list.append(unmatched_track)
                unmatched_track_ids.append(unmatched_track['SPOTIFY'][-22:])
                # print(f"No result found for {playlist_track['ALBUMARTIST']} - {playlist_track['TITLE']}")
                continue
            matched_list += result
            if isinstance(str_to_list(result[0]['PATH']), list):
                # Use the 1st PATH. TODO: Make this more accurate by checking Album
                result[0]['PATH'] = result[0]['PATH'][0]
            matched_paths.append(result[0]['PATH'])

    unmatched_dict = list2dictmerge(deepcopy(unmatched_list))
    matched_dict = list2dictmerge(deepcopy(matched_list))

    print(f"\n{len(matched_list)}/{spotify_playlist_track_total} tracks Matched. ")

    if input("Do you want to generate an m3u file for the matched songs?\nY/N: ") == 'Y':
        generate_m3u(playlist_name=spotify_playlist_name,
                     track_paths=matched_paths)
    if input("Do you want to generate a new spotify playlist for the UNMATCHED songs?\nY/N: ") == 'Y':
        spotify_ops.generate_missing_track_playlist(unmatched_track_ids=unmatched_track_ids,
                                                    playlist_name=spotify_playlist_name)

    with open("unmatched.json", "w") as jsonfile:
        jsonfile.write(json.dumps(unmatched_dict, indent=4, sort_keys=True))
    with open("matched.json", "w") as jsonfile:
        jsonfile.write(json.dumps(matched_dict, indent=4, sort_keys=True))

    db.backup(master)
    master.execute_sql('VACUUM;')


def export_altColumns():
    master = CSqliteExtDatabase(db_path)
    master.backup(db)
    alt_columns = []
    tracks = Music.select().where(
        Music.altALBUM.is_null(False) | Music.altTITLE.is_null(False) | Music.blackALBUM.is_null(
            False) | Music.blackTITLE.is_null(False))
    for row in tracks:
        alt_columns.append(
            {
                'STREAMHASH': row.STREAMHASH,
                'altALBUM': str_to_list(row.altALBUM),
                'blackALBUM': str_to_list(row.blackALBUM),
                'altTITLE': str_to_list(row.altTITLE),
                'blackTITLE': str_to_list(row.blackTITLE)
            }
        )

    with open("altColumns.json", "w") as jsonfile:
        jsonfile.write(json.dumps(alt_columns, indent=4, sort_keys=True))
    db.backup(master)
    master.execute_sql('VACUUM;')


def import_altColumns():
    master = CSqliteExtDatabase(db_path)
    master.backup(db)

    json_file_path = "altColumns.json"
    with open(json_file_path, 'r') as j:
        altColumn = json.loads(j.read())

    for item in altColumn:
        query = Music.update(altALBUM=item['altALBUM'], blackALBUM=item['blackALBUM'], altTITLE=item['altTITLE'],
                             blackTITLE=item['blackTITLE']).where(Music.STREAMHASH == item['STREAMHASH'])
        query.execute()

    db.backup(master)
    master.execute_sql('VACUUM;')


def cleanup_db():
    master = CSqliteExtDatabase(db_path)
    master.backup(db)

    query = Music.select()
    total_tracks = Music.select().count()
    count = 0
    for row in query:
        db_ALBUMARTIST = row.ALBUMARTIST
        db_ARTIST = str_to_list(row.ARTIST)
        db_ALBUM = row.ALBUM
        db_altALBUM = str_to_list(row.altALBUM)
        db_blackALBUM = str_to_list(row.blackALBUM)
        db_TITLE = row.TITLE
        db_altTITLE = str_to_list(row.altTITLE)
        db_blackTITLE = str_to_list(row.blackTITLE)
        db_LYRICS = row.LYRICS
        db_STREAMHASH = row.STREAMHASH
        db_PATH = str_to_list(row.PATH)

        # Remove duplicate paths
        if isinstance(db_PATH, list):
            new_paths = []
            for path in list(set(db_PATH)):
                if os.path.exists(os.path.join(music_root_dir, path)):
                    new_paths.append(path)
            if len(new_paths) == 1:
                db_PATH = new_paths[0]
            else:
                db_PATH = new_paths

        # Handles cases where modifying a tag in a track keeps the old tag in a list.
        if isinstance(db_ALBUM, list):
            if isinstance(db_PATH, list):
                album_list = []
                for paths in db_PATH:
                    track = fetch_metadata_in_background(
                        music_dir=music_root_dir, flac_file=paths)
                    album_list.append(track['ALBUM'])
            else:
                album_list = fetch_metadata_in_background(
                    music_dir=music_root_dir, flac_file=db_PATH)['ALBUM']
            db_ALBUM = album_list

        # These are always List items
        if db_altALBUM is not None:
            db_altALBUM = list(set(db_altALBUM))
            if len(db_altALBUM) == 0:
                db_altALBUM = None
        if db_blackALBUM is not None:
            db_blackALBUM = list(set(db_blackALBUM))
            if len(db_blackALBUM) == 0:
                db_blackALBUM = None
        if db_altTITLE is not None:
            db_altTITLE = list(set(db_altTITLE))
            if len(db_altTITLE) == 0:
                db_altTITLE = None
        if db_blackTITLE is not None:
            db_blackTITLE = list(set(db_blackTITLE))
            if len(db_blackTITLE) == 0:
                db_blackTITLE = None

        update_query = Music.update(ALBUM=db_ALBUM, altALBUM=db_altALBUM, blackALBUM=db_blackALBUM,
                                    altTITLE=db_altTITLE,
                                    blackTITLE=db_blackTITLE, PATH=db_PATH).where(Music.STREAMHASH == db_STREAMHASH)
        update_query.execute()
        count += 1
        print(f"Cleaned {count}/{total_tracks} rows", end="\r")

    db.backup(master)
    master.execute_sql('VACUUM;')


if __name__ == '__main__':
    pass
# else:
#     input("\nPress enter to go back to the main menu")
