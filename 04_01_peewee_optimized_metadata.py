import os
import sqlite3
import subprocess
import time
import zlib
from glob import glob
from itertools import repeat

import pathos.multiprocessing as multiprocessing
import taglib
import tqdm
from peewee import Model
from peewee import TextField
from peewee import CharField
from peewee import BlobField
from peewee import IntegrityError

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


class Music(Model):
    ALBUMARTIST = TextField(index=True)
    ARTIST = TextField(index=True)
    ALBUM = TextField(index=True)
    TITLE = TextField(index=True)
    LYRICS = BlobField(unindexed=True)
    STREAMHASH = CharField(max_length=32, primary_key=True, unique=True)
    PATH = TextField(unindexed=True)

    class Meta:
        database = db


def find_flacs(music_dir):
    print("Scanning directory tree for flac files. Please wait...")
    # for root, dirs, files in os.walk(music_dir, topdown=False):
    #     for file in files:
    #         if file.endswith(".flac"):
    #             flac_files.append(os.path.relpath(os.path.join(root, file), music_dir))
    flac_files = glob("**/*.flac", root_dir=music_dir, recursive=True)

    print("Size of list: " + str(flac_files.__sizeof__()))
    # print(flac_files)
    return flac_files


def asyncmetadata(music_dir, flac_file):
    audiofile = taglib.File(os.path.join(music_dir, flac_file))
    md5sum = subprocess.run(["metaflac", "--show-md5sum", audiofile.path], capture_output=True,
                            universal_newlines=True).stdout.strip()
    audiofile_dict = dict()
    for key in list(audiofile.tags.keys()):
        if len(audiofile.tags[key]) > 1:
            if key == 'ALBUMARTIST':
                """
                Ideally Album artists should be one.
                Multiple Artists should be listed in the Artist tag
                """
                audiofile_dict[key] = audiofile.tags[key][0]
            else:
                audiofile_dict[key] = audiofile.tags[key]
        else:
            if key == "LYRICS":
                audiofile_dict[key] = b64encode(zlib.compress(audiofile.tags[key][0].encode("utf-8"),
                                                              zlib.Z_BEST_COMPRESSION))
            else:
                audiofile_dict[key] = audiofile.tags[key][0]

    audiofile_dict['STREAMHASH'] = md5sum
    audiofile_dict['PATH'] = flac_file
    return audiofile_dict


def generate_metadata(music_dir, flac_files):
    a_pool = multiprocessing.Pool(16)
    # result = a_pool.starmap(fetch_metadata_in_background, zip(repeat(music_dir), flac_files))
    inputs = zip(repeat(music_dir), flac_files)
    # fancy progress bar
    result = a_pool.starmap(asyncmetadata, tqdm.tqdm(inputs, total=len(flac_files)), chunksize=1)
    print(f"Metadata fetched")
    return result


def generate_metadata_single(music_dir, flac_files):
    count = 0
    result = []
    for flac_file in flac_files:
        result.append(asyncmetadata(music_dir, flac_file))
        count = count + 1
    # fancy progress bar
    print(f"Metadata fetched")
    return result


def main():
    music_root_dir = "/Users/rushab.shah/Music/Muzik"

    flac_files = find_flacs(music_root_dir)
    metadata = generate_metadata_single(music_root_dir, flac_files)
    # print(metadata)
    for item in metadata:
        if not "LYRICS" in item:
            item["LYRICS"] = 'NULL'
        album_artist = item['ALBUMARTIST']
        print(f"Current AArtist is {album_artist} of type {type(album_artist)}")
        if not album_artist in filesystem_metadata.keys():
            filesystem_metadata[album_artist] = []
        filesystem_metadata[album_artist].append({
            'ALBUM': item['ALBUM'],
            'ARTIST': item['ARTIST'],
            'TITLE': item['TITLE'],
            'LYRICS': item['LYRICS'],
            'STREAMHASH': item['STREAMHASH'],
            'PATH': item['PATH']
        })

    db.drop_tables([Music])
    db.create_tables([Music])
    music_db_orm = None
    for md in metadata:
        if not "LYRICS" in md:
            md["LYRICS"] = 'NULL'

        # if not "LYRICS" in md:
        #     md["LYRICS"] = 'NULL'
        # else:
        #     md["LYRICS"] = zlib.compress(md['LYRICS'].encode("utf-8"), zlib.Z_BEST_COMPRESSION)
        # print(md["PATH"])
        try:
            music_db_orm = Music.create(ALBUMARTIST=md['ALBUMARTIST'], ARTIST=md['ARTIST'], ALBUM=md['ALBUM'],
                                        TITLE=md['TITLE'], LYRICS=md['LYRICS'], STREAMHASH=md['STREAMHASH'],
                                        PATH=md['PATH'])

        except IntegrityError as IE:
            '''
            Some music files may belong to multiple albums, for ex. "Self titled" and "Greatest hits"
            So we can just query the existing file and convert the relevant columns to a list of values 
            '''
            music_db_orm.save()
            print(f"{bcolors.WARNING}Identical Music found!")
            query = Music.select().where(Music.STREAMHASH == md["STREAMHASH"]).dicts()
            multi_path = []
            multi_album = []
            for row in query:
                if isinstance(row['PATH'], list):
                    multi_path = row['PATH']
                    multi_path.append(md['PATH'])
                else:
                    multi_path.append(row['PATH'])
                    multi_path.append(md['PATH'])
                if isinstance(row['ALBUM'], list):
                    multi_album = row['ALBUM']
                    multi_album.append(md['ALBUM'])
                else:
                    multi_album.append(row['ALBUM'])
                    multi_album.append(md['ALBUM'])
                # print(multi_path)
                query = Music.update(ALBUM=multi_album, PATH=multi_path).where(Music.STREAMHASH == md["STREAMHASH"])
                query.execute()
            print(f"Previous file: {multi_path[0]}\nCurrent file: {multi_path[1]}{bcolors.ENDC}")

    music_db_orm.save()
    db.backup(master)
    master.execute_sql('VACUUM;')
    db.close()
    master.close()
    print("Temp")
    print("Temp")
    print("Temp")
    print("Temp")


if __name__ == '__main__':
    main()

