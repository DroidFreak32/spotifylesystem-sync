import json
import os.path

from peewee import BlobField
from peewee import CharField
from peewee import DoesNotExist
from peewee import ForeignKeyField
from peewee import IntegrityError
from peewee import Model
from peewee import TextField
from playhouse.sqlite_ext import CSqliteExtDatabase

import spotify_ops
from common import bcolors, generate_metadata, list2dictmerge, music_root_dir, db_path
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
    TITLE = TextField(index=True)
    LYRICS = BlobField(unindexed=True, null=True)
    STREAMHASH = CharField(max_length=32, unique=True)
    PATH = TextField(unindexed=True)


def is_item_in_db(db_tag=None, track_tag=None):
    if isinstance(str_to_list(db_tag), list):
        for tag in db_tag:
            if tag.casefold() == track_tag.casefold():
                return True
    if db_tag.casefold() == track_tag.casefold():
        return True
    return False


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
    try:
        # ** here is for case-insensitive matching
        album_artist = AlbumArtist.get(AlbumArtist.ALBUMARTIST ** spotify_album_artist)
    except DoesNotExist:
        return result

    for row in album_artist.tracks:
        if is_item_in_db(row.TITLE, track_metadata['TITLE']):
            if is_item_in_db(row.ALBUM, track_metadata['ALBUM']):
                result.append({
                    'ALBUMARTIST': spotify_album_artist,
                    'PATH': str_to_list(row.PATH),
                    'STREAMHASH': row.STREAMHASH
                })
            else:
                print(f"Spotify track: "
                      f"{track_metadata['ALBUMARTIST']} - {track_metadata['TITLE']}: {track_metadata['SPOTIFY']}\n"
                      f"Track in DB: {row.PATH}\n"
                      f"Are these the same?")
                answer = input("Y/N: ")
                if answer != 'Y' and answer != 'y':
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
                music_db_orm = Music.create(ALBUMARTIST=album_artist, ALBUM=track['ALBUM'],
                                            TITLE=track['TITLE'], ARTIST=track['ARTIST'], LYRICS=track['LYRICS'],
                                            STREAMHASH=track['STREAMHASH'],
                                            PATH=track['PATH'])
            except IntegrityError as IE:
                """
                Some music files may belong to multiple albums, for ex. "Self titled" and "Greatest hits"
                So we can just query the existing file and convert the relevant columns to a list of values 
                """
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
                    query = Music.update(ALBUM=multi_album, PATH=multi_path).where(
                        Music.STREAMHASH == track["STREAMHASH"])
                    query.execute()
                print(f"Previous file: {multi_path[0]}\nCurrent file: {multi_path[1]}{bcolors.ENDC}")
            music_db_orm.save()


def complete_sync(flac_files, db_path):
    flac_files = find_flacs(music_root_dir)
    master = CSqliteExtDatabase(db_path)
    master.backup(db)
    db.drop_tables([AlbumArtist, Music])
    db.create_tables([AlbumArtist, Music])
    metadata = generate_metadata(music_root_dir, flac_files)
    dump_to_db(metadata)
    print("METADATA SYNCED")
    db.backup(master)
    master.execute_sql('VACUUM;')


def partial_sync(flac_files, db_path):
    new_files = []
    db_mtime = os.path.getmtime(db_path)
    for flac_file in flac_files:
        if db_mtime < os.path.getmtime(os.path.join(music_root_dir, flac_file)):
            new_files.append(flac_file)
    print(f"New files: {new_files}")


def generate_playlist():
    master = CSqliteExtDatabase(db_path)
    master.backup(db)
    spotify_playlist_name, spotify_playlist_tracks = spotify_ops.get_playlist()
    matched_list = []
    unmatched_list = []

    for playlist_track in spotify_playlist_tracks:
        result = search_track_in_db(track_metadata=playlist_track)
        if len(result) > 1:
            print(f"Multiple Matches found: {result}")
            # TODO: Ask user for correct match by checking playlist_track['SPOTIFY']
        elif len(result) == 0:
            unmatched_list.append(playlist_track)
            print(f"No result found for {playlist_track['ALBUMARTIST']} - {playlist_track['TITLE']}")
            continue
        matched_list += result

    unmatched_dict = list2dictmerge(unmatched_list)
    matched_dict = list2dictmerge(matched_list)

    print(f"{len(matched_list)}/{len(matched_list)+len(unmatched_list)} tracks Matched. ")

    with open("unmatched.json", "w") as jsonfile:
        jsonfile.write(json.dumps(unmatched_dict, indent=4, sort_keys=True))
    with open("matched.json", "w") as jsonfile:
        jsonfile.write(json.dumps(matched_dict, indent=4, sort_keys=True))


input("INSIDE DB")