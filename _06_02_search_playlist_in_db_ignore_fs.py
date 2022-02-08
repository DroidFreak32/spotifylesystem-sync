import ast
import json
import os
import subprocess
import zlib
from base64 import b64encode
from glob import glob
from itertools import repeat

import pathos.multiprocessing as multiprocessing
import taglib
import tqdm
from peewee import BlobField
from peewee import CharField
from peewee import DoesNotExist
from peewee import ForeignKeyField
from peewee import Model
from peewee import TextField
from playhouse.sqlite_ext import CSqliteExtDatabase

import _05_spotify_fetch as spotify_fetch

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


def str_to_list(unsurestr=None):
    """
    When retreiving a list from DB, it gets saved as a string '["somestring", "somestring2"]'
    This helper function will return such strings as a list or leave it untouched.
    """
    if isinstance(unsurestr, list):
        return unsurestr
    try:
        str2list = ast.literal_eval(unsurestr)
        return str2list
    except:
        return unsurestr


def list2dictmerge(listobj=None):
    """
    A helper to merge all items in list with matching 1st element for ex ->
    [{'ALBUMARTIST': BMTH, 'ALBUM': Sempeternal},  {'ALBUMARTIST': BMTH, 'ALBUM': amo}, ...]
    To a dictionary where the Key is the 1st element:
    {BMTH: [{ALBUM: Sempeternal}, {ALBUM: amo}]
    """
    merged_dict={}

    for tmp in listobj:
        all_keys = list(tmp.keys())
        key = tmp[all_keys[0]]              # First key will be our dictionary's primary key
        if key not in merged_dict.keys():
            merged_dict[key] = []           # Create the primary key dictionary { 'BMTH': [] }
        tmp.pop(all_keys[0])                # Remove redundant primary key before adding it to the dictionary.
        merged_dict[key].append(tmp)

    return merged_dict


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

    if md5sum == "00000000000000000000000000000000":
        print(f"FLAC file {audiofile.path} possibly corrupted. STREAMHASH is 000..!")
        md5sum = subprocess.run(["md5sum", audiofile.path], capture_output=True,
                            universal_newlines=True).stdout.strip()
        md5sum = md5sum[0:32]
        
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
    music_root_dir = "/home/horcrux/Music/Muzik"


    # =============== TODO: SEPARATE SPOTIFY INTEGRATION FILE NEEDED ===============
    # =============== TODO: For each unmatched result check for a whitelist file to resolve known false-negatives

    spot_playlist_tracks = spotify_fetch.main()

    tmp = 0

    def search_track_in_db(track_metadata=None):
        """
        Scans the DB for a given spotify track and returns a match or an empty list.
        :param track_metadata:
        :return:
        """
        result = []
        spotify_album_artist = track_metadata['ALBUMARTIST']
        try:
            # ** here is for case insensitive matching
            album_artist = AlbumArtist.get(AlbumArtist.ALBUMARTIST ** spotify_album_artist)
        except DoesNotExist:
            return result

        for row in album_artist.tracks:
            if row.TITLE.casefold() == track_metadata['TITLE'].casefold():
                result.append({
                    'ALBUMARTIST': spotify_album_artist,
                    'PATH': str_to_list(row.PATH),
                    'STREAMHASH': row.STREAMHASH
                })
                # if spotify_album_artist not in result.keys():
                #     result[spotify_album_artist] = []
                #
                # result[spotify_album_artist].append({
                #     'PATH': str_to_list(row.PATH),
                #     'STREAMHASH': row.STREAMHASH
                # })
        return result

    matched_list = []
    unmatched_list = []
    for playlist_track in spot_playlist_tracks:
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

    print(f"{len(matched_list)}/{len(unmatched_list)+len(unmatched_list)} tracks Matched. ")

    with open("unmatched.json", "w") as jsonfile:
        jsonfile.write(json.dumps(unmatched_dict, indent=4, sort_keys=True))
    with open("matched.json", "w") as jsonfile:
        jsonfile.write(json.dumps(matched_dict, indent=4, sort_keys=True))

    db.close()
    master.close()


if __name__ == '__main__':
    main()
