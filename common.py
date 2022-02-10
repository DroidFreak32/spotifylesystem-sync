import argparse
import ast
import os
import zlib
from base64 import b64encode
import subprocess
from itertools import repeat

import spotipy
import glob

from configparser import ConfigParser

import pathos.multiprocessing as multiprocessing
import taglib
import tqdm
from spotipy import SpotifyOAuth

global music_root_dir
global db_path
global spotify_client_id
global spotify_client_secret
global redirect_uri

config = ConfigParser()
config.read("config.ini")

parser = argparse.ArgumentParser()
parser.add_argument('--music-dir', type=str, help='Path to the music directory', required=False)
parser.add_argument('--db-path', type=str, help='Path to the music db file', required=False)
parser.add_argument('--spotify-client-id', type=str, help='Your spotify client ID', required=False)
parser.add_argument('--spotify-client-secret', type=str, help='Your spotify client secret', required=False)
parser.add_argument('--redirect-uri', type=str, help='Spotify redirect-uri', required=False)
args, leftovers = parser.parse_known_args()

if args.music_dir is not None:
    music_root_dir = os.path.expanduser(args.music_dir)
else:
    music_root_dir = os.path.expanduser(config['DEFAULT']['music-dir'])

if args.db_path is not None:
    db_path = os.path.expanduser(args.db_path)
else:
    db_path = config['DEFAULT']['musicdb']

if args.spotify_client_id is not None:
    spotify_client_id = args.spotify_client_id
else:
    spotify_client_id = config['DEFAULT']['spotify-client']

if args.spotify_client_secret is not None:
    spotify_client_secret = args.spotify_client_secret
else:
    spotify_client_secret = config['DEFAULT']['spotify-secret']

if args.redirect_uri is not None:
    redirect_uri = args.redirect_uri
else:
    redirect_uri = config['DEFAULT']['redirect-uri']

print(music_root_dir)
print(db_path)
print(spotify_client_id)
print(spotify_client_secret)
print(redirect_uri)

print("I am inside common")


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


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_spotify_connection():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotify_client_id,
                                                   client_secret=spotify_client_secret,
                                                   redirect_uri=redirect_uri,
                                                   scope="user-library-read"))
    return sp

def str_to_list(unsurestr=None):
    """
    When retreiving a list from DB, it gets saved as a string '["somestring", "somestring2"]'
    This helper function will return such strings as a list or leave it untouched.
    TODO: Maybe another to just return a list and use 'is in' condition? Casefold may be an issue though
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
    merged_dict = {}

    for tmp in listobj:
        all_keys = list(tmp.keys())
        key = tmp[all_keys[0]]  # First key will be our dictionary's primary key
        if key not in merged_dict.keys():
            merged_dict[key] = []  # Create the primary key dictionary { 'BMTH': [] }
        tmp.pop(all_keys[0])  # Remove redundant primary key before adding it to the dictionary.
        merged_dict[key].append(tmp)

    return merged_dict


def find_flacs(music_dir):
    print("Scanning directory tree for flac files. Please wait...")
    # for root, dirs, files in os.walk(music_dir, topdown=False):
    #     for file in files:
    #         if file.endswith(".flac"):
    #             flac_files.append(os.path.relpath(os.path.join(root, file), music_dir))
    flac_files = glob.glob("**/*.flac", root_dir=music_dir, recursive=True)

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

input("INSIDE COMMON")
if __name__ == '__main__':
    print("Main")

