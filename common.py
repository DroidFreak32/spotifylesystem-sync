import argparse
import ast
import glob
import os
import platform
import re
import subprocess
import zlib
from base64 import b64encode
from configparser import ConfigParser
from datetime import datetime
from itertools import repeat

import pathos.multiprocessing as multiprocessing
import spotipy
import taglib
import tqdm
from spotipy import SpotifyOAuth

global music_root_dir
global db_path
global db_mtime_marker
global spotify_client_id
global spotify_client_secret
global redirect_uri
global multitag_files


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

multitag_files = []

common_regex = r' \([12][0-9]{3}.+[Rr]emas.*\)| \([Rr]emaster.*\)| - [Rr]emas.*| - [12][0-9]{3}.+[Rr]emas.*| [Rr]emast.*| [12][0-9]{3}.+[Rr]emas.*| \(feat.*\)'

instrumental_lyric = [b'eNrzzCsuKSrNTc0rScwBACBQBQc=']

config = ConfigParser()
config.read("config.ini")
config_template = f"{bcolors.OKCYAN}[DEFAULT]" \
    f"\nmusic-dir={bcolors.ENDC}<path/to/root/music/folder>" \
    f"\n{bcolors.OKCYAN}db-name={bcolors.ENDC}<name_of_database_file>.sb" \
    f"\n{bcolors.OKCYAN}SPOTIFY_CLIENT_ID={bcolors.ENDC}<From your spotify dev console>" \
    f"\n{bcolors.OKCYAN}SPOTIFY_CLIENT_SECRET={bcolors.ENDC}<From your spotify dev console>" \
    f"\n{bcolors.OKCYAN}redirect-uri={bcolors.ENDC}http://127.0.0.1:9090"

parser = argparse.ArgumentParser()
parser.add_argument('--music-dir', type=str, help='Path to the music directory', required=False)
parser.add_argument('--db-name', type=str, help='Name of the music db file', required=False)
parser.add_argument('--spotify-client-id', type=str, help='Your spotify client ID', required=False)
parser.add_argument('--spotify-client-secret', type=str, help='Your spotify client secret', required=False)
parser.add_argument('--redirect-uri', type=str, help='Spotify redirect-uri', required=False)
args, leftovers = parser.parse_known_args()

if args.music_dir is not None:
    music_root_dir = os.path.expanduser(args.music_dir)
else:
    try:
        music_root_dir = os.path.expanduser(config['DEFAULT']['music-dir'])
    except KeyError:
        print(f"{bcolors.WARNING}config.ini file missing or incorrect!"
              f"\nPlease create config.ini inside this projects root directory with the following template:{bcolors.ENDC}"
              f"\n****************************"
              f"\n{config_template}"
              f"\n****************************\n")
        exit()

if args.db_name is not None:
    db_path = os.path.join(music_root_dir, args.db_name)
    db_mtime_marker = os.path.join(music_root_dir, '.' + args.db_name + '.marker')
else:
    db_path = os.path.join(music_root_dir, config['DEFAULT']['db-name'])
    db_mtime_marker = os.path.join(music_root_dir, '.' + config['DEFAULT']['db-name'] + '.marker')

if args.spotify_client_id is not None:
    spotify_client_id = args.spotify_client_id
else:
    spotify_client_id = config['DEFAULT']['SPOTIFY_CLIENT_ID']

if args.spotify_client_secret is not None:
    spotify_client_secret = args.spotify_client_secret
else:
    spotify_client_secret = config['DEFAULT']['SPOTIFY_CLIENT_SECRET']

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



def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def openfile(filepath=None):
    #TODO: Dont supress error
    # https://stackoverflow.com/a/435669/6437140
    if not os.path.exists(filepath):
        print(f"{bcolors.FAIL}Invalid Path!{bcolors.ENDC}")
        return
    print(f"Opening: {filepath}")
    if platform.system() == 'Linux':  # Linux
        subprocess.call(('xdg-open', filepath), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    elif platform.system() == 'Windows':  # Windows
        os.startfile(filepath)
    else:  # macOS
        subprocess.call(('open', filepath))


def play_files_in_order(paths=None):
    paths = str_to_list(paths)
    if isinstance(paths, list):
        if len(paths) > 1:
            print(f"Multiple files found!")
            while True:
                print("\nSelect the file number to play or enter Q to quit:")
                index = 1
                for file in paths:
                    print(f"{index}) {file}")
                    index += 1
                id = input("> ")
                if id[0].casefold() == 'q':
                    print(f"Going back..")
                    return
                elif id.isdigit():
                    id = int(id)
                    if id <= len(paths):
                        full_path=os.path.join(music_root_dir, paths[id-1])
                        openfile(full_path)
                    else:
                        print(f"Invalid Input!")
                else:
                    print(f"Invalid Input!")
        else:
            full_path = os.path.join(music_root_dir, paths[0])
            openfile(full_path)
    else:
        full_path = os.path.join(music_root_dir, paths)
        openfile(full_path)
    return


def get_spotify_connection():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotify_client_id,
                                                   client_secret=spotify_client_secret,
                                                   redirect_uri=redirect_uri,
                                                   scope="user-library-read playlist-modify-private "
                                                         "playlist-read-private playlist-read-collaborative"))

    return sp

def get_current_datetime(format_string='%Y%m%d_%H%M'):
    return datetime.today().strftime(format_string)


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

    merged_dict = dict(sorted(merged_dict.items()))
    return merged_dict


def find_flacs(music_dir=None):
    print("Scanning directory tree for flac files. Please wait...")
    # for root, dirs, files in os.walk(music_dir, topdown=False):
    #     for file in files:
    #         if file.endswith(".flac"):
    #             flac_files.append(os.path.relpath(os.path.join(root, file), music_dir))
    flac_files = glob.glob("**/*.flac", root_dir=music_dir, recursive=True)
    return flac_files


def missing_lrc(flacs=None):
    if flacs is None:
        flacs = find_flacs(music_root_dir)
    missing_lrcs = []
    for file in flacs:

        if not os.path.exists(
            os.path.join(
                music_root_dir, os.path.splitext(file)[0] + '.lrc'
            )
        ):
            tempvar = fetch_metadata_in_background(flac_file=file)
            # Ignore Instrumentals!!
            if tempvar['LYRICS'] in instrumental_lyric:
                continue
            missing_lrcs.append(file)
    return missing_lrcs

def is_title_a_known_mismatch(db_track=str(), spotify_track=str()):
    if db_track == re.sub(common_regex, '', spotify_track) or spotify_track == re.sub(common_regex, '', db_track):
        return True
    return False



def get_last_flac_mtime(flac_files=[]):
    last_flac_mtime = os.path.getmtime(os.path.join(music_root_dir, flac_files[0]))
    for file_path in flac_files:
        file_mtime = os.path.getmtime(os.path.join(music_root_dir, file_path))
        if file_mtime > last_flac_mtime:
            last_flac_mtime = file_mtime
    return last_flac_mtime


def fetch_metadata_in_background(music_dir=music_root_dir, flac_file=None):
    """
    Gets & generates all the required metadata for a flac track.
    :param multitag_files:
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
        # This print was for debugging
        # print(f"\n{bcolors.WARNING}Multiple Album Artists: {audiofile.tags['ALBUMARTIST']} in track.\n"
        #       f"Only storing the first one: {audiofile.tags['ALBUMARTIST'][0]}\nCheck "
        #       f"{bcolors.ENDC}{bcolors.BOLD}{bcolors.UNDERLINE}{flac_file}.{bcolors.ENDC}")

        audiofile_dict['multitag'] = flac_file

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
        audiofile_dict['LYRICS'] = None
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
    warning_flag = False
    metadata_result = {}
    a_pool = multiprocessing.Pool(4)
    # result = a_pool.starmap(fetch_metadata_in_background, zip(repeat(music_dir), flac_files))
    inputs = zip(repeat(music_dir), flac_files)

    # fancy progress bar
    result = a_pool.starmap(fetch_metadata_in_background, tqdm.tqdm(inputs, total=len(flac_files)), chunksize=1)
    print(f"\nMetadata fetched!\n")

    for item in result:
        # Create a list of files having multiple albumartists
        if 'multitag' in item.keys():
            multitag_files.append(item['multitag'])
            item.pop('multitag')
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

    if len(multitag_files) > 0:
        warning_flag = True
        print(f"{bcolors.BOLD}{bcolors.WARNING}These files have multiple album artists:\n{bcolors.ENDC}")
        print(multitag_files)
        answer = input(f"{bcolors.BOLD}{bcolors.WARNING}Generate a playlist for easy import into mp3tag, foobar2k "
                       f"etc? (Y/N){bcolors.ENDC}\n")
        if answer == 'Y' or answer == 'y':
            generate_m3u('fixme_multiple_albumartists', multitag_files)
    return metadata_result, warning_flag


def generate_m3u(playlist_name='playlist', track_paths=[]):
    location = os.path.join(music_root_dir, playlist_name + '.m3u')
    with open(location, 'w', encoding='utf-8') as p:
        print(f"#EXTM3U\n#PLAYLIST:{playlist_name}", file=p)
        for item in track_paths:
            print(item, file=p)
    print("\nPlaylist generated at: " + location)


if __name__ == '__main__':
    flacs = find_flacs(music_root_dir)
    non_lrc_files = missing_lrc(flacs)
    generate_m3u(playlist_name="LyricsMissing", track_paths=non_lrc_files)
    print("Main")
