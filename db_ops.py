from copy import copy, deepcopy

from importlib.resources import path
import json
import os
from urllib import request
from pathlib import Path

from peewee import BlobField
from peewee import CharField
from peewee import DoesNotExist
from peewee import ForeignKeyField
from peewee import IntegrityError
from peewee import Model
from peewee import TextField
from playhouse.sqlite_ext import CSqliteExtDatabase

import spotify_ops
from common import bcolors, generate_m3u, generate_metadata, get_last_flac_mtime, list2dictmerge, music_root_dir, db_path, db_mtime_marker
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

    print(f"\n{bcolors.OKGREEN}Adding {altALBUM_to_add} to alt Albums{bcolors.ENDC}\n")
    query = Music.update(altALBUM = altALBUM_to_add).where(Music.STREAMHASH == db_row.STREAMHASH)
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

    print(f"\n{bcolors.OKGREEN}Adding {altTITLE_to_add} to alt Titles{bcolors.ENDC}\n")
    query = Music.update(altTITLE = altTITLE_to_add).where(Music.STREAMHASH == db_row.STREAMHASH)
    query.execute()


def add_to_black_album(db_row, track_metadata):
    blackALBUM_to_add = str_to_list(db_row.blackALBUM)
    # TODO: This is just a POC. add more functions to get existing values/lists before adding
    if isinstance(blackALBUM_to_add, list):
        blackALBUM_to_add.append(track_metadata['ALBUM'])
    else:
        blackALBUM_to_add = [track_metadata['ALBUM']]

    print(f"\n{bcolors.HEADER}Adding {blackALBUM_to_add} to blacklist{bcolors.ENDC}\n")
    query = Music.update(blackALBUM = blackALBUM_to_add).where(Music.STREAMHASH == db_row.STREAMHASH)
    query.execute()


def add_to_black_title(db_row, track_metadata):
    blackTITLE_to_add = str_to_list(db_row.blackTITLE)
    # TODO: This is just a POC. add more functions to get existing values/lists before adding
    if isinstance(blackTITLE_to_add, list):
        blackTITLE_to_add.append(track_metadata['TITLE'])
    else:
        blackTITLE_to_add = [track_metadata['TITLE']]

    print(f"\n{bcolors.HEADER}Adding {blackTITLE_to_add} to blacklist{bcolors.ENDC}\n")
    query = Music.update(blackTITLE = blackTITLE_to_add).where(Music.STREAMHASH == db_row.STREAMHASH)
    query.execute()


def search_track_in_db(track_metadata=None):
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
    spotify_album_artist = track_metadata['ALBUMARTIST']
    if spotify_album_artist.casefold() == 'Halsey':
        pass
    try:
        # ** here is for case-insensitive matching
        album_artist = AlbumArtist.get(AlbumArtist.ALBUMARTIST ** spotify_album_artist)
    except DoesNotExist:
        return result

    for row in album_artist.tracks:
        db_title = deepcopy(row.TITLE.casefold())
        spotify_title = deepcopy(track_metadata['TITLE'].casefold())

        db_album = deepcopy(row.ALBUM.casefold())
        spotify_album = deepcopy(track_metadata['ALBUM'].casefold())



        if db_title in spotify_title or is_title_in_alt_title(db_row=row, track_metadata=track_metadata):
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
                    f"\nAre these the same?\n")
                answer = input("Y/N: ")
                if answer == 'Y' or answer == 'y':
                    print(f"*** Ignoring Title ***")
                    add_to_alt_title(db_row=row, track_metadata=track_metadata)
                else:
                    add_to_black_title(db_row=row, track_metadata=track_metadata)

            if db_title == spotify_title or is_title_in_alt_title(db_row=row, track_metadata=track_metadata):
                if is_item_in_db_column(row.ALBUM, track_metadata['ALBUM']) or is_album_in_alt_album(db_row=row, track_metadata=track_metadata):
                    result.append({
                        'ALBUMARTIST': spotify_album_artist,
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
                        f"\nAre these the same?\n")
                    answer = input("Y/N: ")
                    
                    if answer == 'n' or answer == 'N':
                        add_to_black_album(row, track_metadata)
                        continue

                    if answer == 'Y' or answer == 'y':
                        add_to_alt_album(row, track_metadata)
                        result.append({
                            'ALBUMARTIST': spotify_album_artist,
                            'PATH': str_to_list(row.PATH),
                            'STREAMHASH': row.STREAMHASH
                        })
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
            album_artist = AlbumArtist.get(AlbumArtist.ALBUMARTIST == album_artists)
            try:
                music_db_orm = Music.create(ALBUMARTIST=album_artist, ARTIST=track['ARTIST'], ALBUM=track['ALBUM'], altALBUM=None, blackALBUM=None,
                                            TITLE=track['TITLE'], altTITLE=None, blackTITLE=None, LYRICS=track['LYRICS'],
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
                query = Music.select().where(Music.STREAMHASH == track["STREAMHASH"]).dicts()
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
                        print(f"{bcolors.WARNING}Is this file a duplicate copy?{bcolors.ENDC}")
                        multi_album = track['ALBUM']
                    else:
                        multi_album.append(row['ALBUM'])
                        multi_album.append(track['ALBUM'])
                    # print(multi_path)
                    query = Music.update(ALBUMARTIST=album_artist, ARTIST=track['ARTIST'], ALBUM=multi_album, altALBUM=row['altALBUM'], blackALBUM=row['blackALBUM'],
                                        TITLE=track['TITLE'], altTITLE=row['altTITLE'], blackTITLE=row['blackTITLE'], LYRICS=track['LYRICS'],
                                        PATH=multi_path).where(Music.STREAMHASH == track["STREAMHASH"])
                    query.execute()
                print(f"Previous file: {multi_path[0]}\nCurrent file: {multi_path[1]}{bcolors.ENDC}")
    music_db_orm.save()


def sync_fs_to_db(force_resync=True, flac_files=find_flacs(music_root_dir), last_flac_mtime=1):

    master = CSqliteExtDatabase(db_path)
    master.backup(db)
    if force_resync:
        last_flac_mtime = get_last_flac_mtime(flac_files)
        db.drop_tables([AlbumArtist, Music])
        db.create_tables([AlbumArtist, Music])

    metadata = generate_metadata(music_root_dir, flac_files)
    dump_to_db(metadata)
    print("METADATA SYNCED")
    db.backup(master)
    master.execute_sql('VACUUM;')
    Path(db_mtime_marker).touch()
    os.utime(db_mtime_marker, (last_flac_mtime, last_flac_mtime))
    print(os.path.getmtime(db_mtime_marker))



def partial_sync():
    flac_files = find_flacs(music_root_dir)
    new_files = []
    db_mtime = os.path.getmtime(db_mtime_marker)
    for flac_file in flac_files:
        if db_mtime < os.path.getmtime(os.path.join(music_root_dir, flac_file)):
            new_files.append(flac_file)
    print(f"New files: {new_files}")
    if len(new_files) > 0:
        sync_fs_to_db(force_resync=False, flac_files=new_files, last_flac_mtime=db_mtime)


def generate_playlist():
    master = CSqliteExtDatabase(db_path)
    master.backup(db)
    spotify_playlist_name, spotify_playlist_tracks = spotify_ops.get_playlist()
    matched_list = []
    matched_paths = []
    unmatched_list = []

    for playlist_track in spotify_playlist_tracks:
        result = search_track_in_db(track_metadata=playlist_track)
        if len(result) > 1:
            print(f"{bcolors.FAIL}Multiple Matches found: {result}{bcolors.ENDC}")
            # TODO: Ask user for correct match by checking playlist_track['SPOTIFY']
            continue
        elif len(result) == 0:
            unmatched_list.append(playlist_track)
            # print(f"No result found for {playlist_track['ALBUMARTIST']} - {playlist_track['TITLE']}")
            continue
        matched_list += result
        if isinstance(str_to_list(result[0]['PATH']), list):
            result[0]['PATH'] = result[0]['PATH'][0]
        matched_paths.append(result[0]['PATH'])

    unmatched_dict = list2dictmerge(unmatched_list)
    matched_dict = list2dictmerge(matched_list)

    print(f"{len(matched_list)}/{len(matched_list)+len(unmatched_list)} tracks Matched. ")

    generate_m3u(playlist_name=spotify_playlist_name, track_paths=matched_paths)

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
    tracks = Music.select().where( Music.altALBUM.is_null(False) | Music.altTITLE.is_null(False) | Music.blackALBUM.is_null(False) | Music.blackTITLE.is_null(False) )
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
        query = Music.update(altALBUM = item['altALBUM'], blackALBUM = item['blackALBUM'], altTITLE = item['altTITLE'], blackTITLE = item['blackTITLE']).where(Music.STREAMHASH == item['STREAMHASH'])
        query.execute()
    
    db.backup(master)
    master.execute_sql('VACUUM;')

if __name__ == '__main__':
    print("Use spotifylesystem-sync.py")
