import os
import sqlite3
import subprocess
import time
import zlib
from glob import glob
from itertools import repeat
import _05_spotify_fetch as spotify_fetch

import pathos.multiprocessing as multiprocessing
import taglib
import tqdm
from peewee import Model
from peewee import TextField
from peewee import CharField
from peewee import BlobField
from peewee import ForeignKeyField
from peewee import IntegrityError
from peewee import DoesNotExist

from playhouse.sqlite_ext import CSqliteExtDatabase
from base64 import b64encode
from base64 import b64decode

master = CSqliteExtDatabase("test.db")
db = CSqliteExtDatabase(":memory:")
master.backup(db)
filesystem_metadata = dict()


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
    LYRICS = BlobField(unindexed=True)
    STREAMHASH = CharField(max_length=32, unique=True)
    PATH = TextField(unindexed=True)


def find_flacs(music_dir):
    print("Scanning directory tree for flac files. Please wait...")
    # for root, dirs, files in os.walk(music_dir, topdown=False):
    #     for file in files:
    #         if file.endswith(".flac"):
    #             flac_files.append(os.path.relpath(os.path.join(root, file), music_dir))
    flac_files = glob("**/*.flac", root_dir=music_dir, recursive=True)

    print("Size of list: " + str(flac_files.__sizeof__()))

    return flac_files


def fetch_metadata_in_background(music_dir, flac_file):
    """
    Gets & generates all the required metadata for a flac track.
    :param music_dir: Root music directory
    :param flac_file: Relative path to the flac file from root
    :return: A dictionary of track's relevant metadata
    """
    audiofile = taglib.File(os.path.join(music_dir, flac_file))
    md5sum = subprocess.run(["metaflac", "--show-md5sum", audiofile.path], capture_output=True,
                            universal_newlines=True).stdout.strip()
    audiofile_dict = dict()

    if len(audiofile.tags['ALBUMARTIST']) > 1:
        """
        Ideally ALBUMARTIST should be just one.
        Multiple artists should be listed in the ARTIST tag
        """
        print(f"\n{bcolors.FAIL}Multiple Album Artists: {audiofile.tags['ALBUMARTIST']} in track.\n"
              f"Only storing the first one: {audiofile.tags['ALBUMARTIST'][0]}\n"
              f"Check {flac_file}.{bcolors.ENDC}")

    audiofile_dict['ALBUMARTIST'] = audiofile.tags['ALBUMARTIST'][0]

    """
    For Artists, it is OK to have multiple artists (feat. Artists) in a track.
    Store as a list of multiple artists are involved, else string.
    """
    if len(audiofile.tags['ARTIST']) > 1:
        audiofile_dict['ARTIST'] = audiofile.tags["ARTIST"]
    else:
        audiofile_dict['ARTIST'] = audiofile.tags["ARTIST"][0]

    # """
    # Store each Album Artist as the Key whose value is the list of all their tracks.
    # This will also be the primary key in the DB
    # """
    # if not album_artist in audiofile_dict.keys():
    #     audiofile_dict[album_artist] = []

    """
    Compressing lyrics to save space in the DB.
    TODO: Remove base64 conversion
    """
    if 'LYRICS' not in audiofile.tags:
        audiofile_dict['LYRICS'] = 'NULL'
    else:
        audiofile_dict['LYRICS'] = b64encode(zlib.compress(audiofile.tags['LYRICS'][0].encode("utf-8"),
                                                           zlib.Z_BEST_COMPRESSION))

    # Remaining track tags:
    audiofile_dict['ALBUM'] = audiofile.tags['ALBUM'][0]
    audiofile_dict['TITLE'] = audiofile.tags['TITLE'][0]
    audiofile_dict['STREAMHASH'] = md5sum
    audiofile_dict['PATH'] = flac_file

    return audiofile_dict


def generate_metadata(music_dir, flac_files):
    """
    Accumulates all relevant metadata from a list of flac files
    :param music_dir: Root music directory
    :param flac_files: List of flac files
    :return: A dictionary with key=AlbumArtist and Value=[metadata of all their tracks]
    """
    metadata_result = {}
    a_pool = multiprocessing.Pool(12)
    # result = a_pool.starmap(fetch_metadata_in_background, zip(repeat(music_dir), flac_files))
    inputs = zip(repeat(music_dir), flac_files)

    # fancy progress bar
    result = a_pool.starmap(fetch_metadata_in_background, tqdm.tqdm(inputs, total=len(flac_files)), chunksize=1)
    print(f"Metadata fetched")

    for item in result:
        album_artist = item['ALBUMARTIST']
        if album_artist not in metadata_result.keys():
            metadata_result[album_artist] = []

        metadata_result[album_artist].append({
            'ALBUM': item['ALBUM'],
            'ARTIST': item['ARTIST'],
            'TITLE': item['TITLE'],
            'LYRICS': item['LYRICS'],
            'STREAMHASH': item['STREAMHASH'],
            'PATH': item['PATH']
        })
    return metadata_result


def generate_metadata_single_thread(music_dir, flac_files):
    count = 0
    metadata_result = {}
    result = []
    for flac_file in flac_files:
        result.append(fetch_metadata_in_background(music_dir, flac_file))
        count = count + 1
        # fancy progress bar
        print(f"{count} of {len(flac_files)} Metadata fetched", end='\r')

    for item in result:
        album_artist = item['ALBUMARTIST']
        if album_artist not in metadata_result.keys():
            metadata_result[album_artist] = []

        metadata_result[album_artist].append({
            'ALBUM': item['ALBUM'],
            'ARTIST': item['ARTIST'],
            'TITLE': item['TITLE'],
            'LYRICS': item['LYRICS'],
            'STREAMHASH': item['STREAMHASH'],
            'PATH': item['PATH']
        })
    return metadata_result


def main():
    music_root_dir = "/Users/rushab.shah/Music/Muzik"

    flac_files = find_flacs(music_root_dir)
    metadata = generate_metadata(music_root_dir, flac_files)

    db.drop_tables([AlbumArtist, Music])
    db.create_tables([AlbumArtist, Music])
    music_db_orm = None

    for album_artists, track_list in metadata.items():
        AlbumArtist.create(ALBUMARTIST=album_artists)
        for track in track_list:
            """
            Get an AlbumArtist object, maybe for backref?? Blind copy pasta
            """
            album_artist = AlbumArtist.get(AlbumArtist.ALBUMARTIST == album_artists)
            try:
                music_db_orm = Music.create(ALBUMARTIST=album_artist, ARTIST=track['ARTIST'], ALBUM=track['ALBUM'],
                                            TITLE=track['TITLE'], LYRICS=track['LYRICS'],
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
                    Either append to existing Albums & Paths
                    or convert to a list of Albums and Paths
                    """

                    if isinstance(row['PATH'], list):
                        multi_path = row['PATH']
                        multi_path.append(track['PATH'])
                    else:
                        multi_path.append(row['PATH'])
                        multi_path.append(track['PATH'])
                    if isinstance(row['ALBUM'], list):
                        multi_album = row['ALBUM']
                        multi_album.append(track['ALBUM'])
                    else:
                        multi_album.append(row['ALBUM'])
                        multi_album.append(track['ALBUM'])
                    # print(multi_path)
                    query = Music.update(ALBUM=multi_album, PATH=multi_path).where(
                        Music.STREAMHASH == track["STREAMHASH"])
                    query.execute()
                print(f"Previous file: {multi_path[0]}\nCurrent file: {multi_path[1]}{bcolors.ENDC}")

    """
    Now we can query tracks from individual artists:
    
    artist = AlbumArtist.get(AlbumArtist.ALBUMARTIST == "Linkin Park")
    for row in artist.tracks:
        if row.TITLE == playlist_track['TITLE']:
        print(row.PATH)
        
    """
    music_db_orm.save()
    db.backup(master)
    master.execute_sql('VACUUM;')

    spot_playlist_tracks = spotify_fetch.main()

    tmp=0

    def search_track_in_db(track_metadata=None):
        result = []
        try:
            album_artist = AlbumArtist.get(AlbumArtist.ALBUMARTIST == track_metadata['ALBUMARTIST'])
        except DoesNotExist:
            return result

        for row in album_artist.tracks:
            if row.TITLE == track_metadata['TITLE']:
                result.append({
                    'PATH': row.PATH,
                    'STREAMHASH': row.STREAMHASH
                })
        return result

    matched_list = []
    for playlist_track in spot_playlist_tracks:
        result = search_track_in_db(track_metadata=playlist_track)
        if len(result) > 1:
            print(f"Multuple Matches found: {result}")
        elif len(result) == 0:
            print(f"No result found for {playlist_track['ALBUMARTIST']} - {playlist_track['TITLE']}")
            continue
        else:
            matched_list.append(result)
    print(matched_list)

    tmp=0



    db.close()
    master.close()


if __name__ == '__main__':
    main()
