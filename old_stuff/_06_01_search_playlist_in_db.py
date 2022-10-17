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
from peewee import IntegrityError
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
    LYRICS = BlobField(unindexed=True, null=True)
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
        # ** here is for case insensitive matching
        album_artist = AlbumArtist.get(AlbumArtist.ALBUMARTIST ** spotify_album_artist)
    except DoesNotExist:
        return result

    for row in album_artist.tracks:
        if row.TITLE.casefold() == track_metadata['TITLE'].casefold():
            if row.ALBUM.casefold() in track_metadata['ALBUM'].casefold():
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

# @DeprecationWarning
# def search_track_in_db_nostage(track_metadata=None, album_artist=None):
#     """
#     Scans the DB for a given spotify track and returns a match or an empty list.
#         - First perform a case-insensitive match of the AlbumArtist
#         - Match the title of track
#         - Match the album if title matches to avoid duplicate matches!
#             - TODO: Separate logging for such tracks
#     :param album_artist:
#     :param track_metadata: A spotify track
#     :return: Matched item's PATH & STREAMHASH from database.
#     """
#     result = []
#     spotify_title = deepcopy(track_metadata['TITLE'].casefold())
#     spotify_album = deepcopy(track_metadata['ALBUM'].casefold())
#
#     def safe_title_substring(_db_title='test', _spotify_title='test'):
#         """
#         On many cases the title we need is already a substring of Spotify's title
#         This function matches these, without too many false positive matches on shorter titles.
#         10 characters matching should be a good sweet spot to avoid false positives like
#         Ex: "AbcArtist - SHORT.flac" should not match "AbcArtist - This is not a SHORTER title.flac"
#         """
#         if len(_db_title) > 10 and _db_title.casefold() in _spotify_title.casefold():
#             return True
#         return False
#
#     def check_live_tracks_mismatch(_db_title='test', _spotify_title='test'):
#         if ('live' in _db_title) or ('live' in _spotify_title):
#             if ('live' in _db_title) and ('live' in _spotify_title):
#                 return False
#             else:
#                 return True
#         return False
#
#     tempvar = []
#     for row in album_artist.tracks:
#         tempvar.append(row)
#
#     for row in album_artist.tracks:
#         # Reset these flags in each iteration
#         bypass_title = False
#         bypass_album = False
#
#         db_title = deepcopy(row.TITLE.casefold())
#
#         db_album = deepcopy(row.ALBUM.casefold())
#
#         if fuzz.ratio(db_title, spotify_title) >= 85 \
#                 or is_title_in_alt_title(db_row=row, track_metadata=track_metadata) \
#                 or spotify_title == db_title or safe_title_substring(db_title, spotify_title) \
#                 or is_title_a_known_mismatch(db_title, spotify_title):
#             # For ex "The Diary of Jane" is in "The Diary of Jane - Single Version" so match such cases too.
#
#             if check_live_tracks_mismatch(db_title, spotify_title) and not is_title_in_alt_title(db_row=row, track_metadata=track_metadata):
#                 # If the track is a live version but the DB doesn't contain that string, unmatch immediately.
#                 # Skips unnecessary matches of live versions with studio versions
#                 continue
#
#             if is_item_in_db_column(row.blackTITLE, track_metadata['TITLE']):
#                 # This track is probably another edition, i.e. Acoustic Version
#                 # If subsequent iterations do not get this track then it will be a part of unmatched list.
#                 continue
#
#             if is_item_in_db_column(row.blackALBUM, track_metadata['ALBUM']):
#                 # This track belongs to another existing album in the DB, or we do not have it.
#                 # If subsequent iterations do not get this track then it will be a part of unmatched list.
#                 continue
#             if db_title != spotify_title and not is_title_in_alt_title(db_row=row, track_metadata=track_metadata):
#                 """
#                 We don't have an exact match, so prompt user to verify and update alternate / blacklist tags in DB.
#                 """
#                 message = \
#                     f"\nSpotify URL: {track_metadata['SPOTIFY']}" \
#                     f"\nSpotify / DB Title:" \
#                     f"\n{bcolors.OKGREEN}" \
#                     f"{track_metadata['TITLE']}{bcolors.ENDC} / {bcolors.OKCYAN}{row.TITLE}" \
#                     f"{bcolors.ENDC}" \
#                     f"\n\nPATH {row.PATH}" \
#                     f"\n\nAre these the same?" \
#                     f"\n(Y)es, this is an alternate title." \
#                     f"\n(B)lacklist {bcolors.OKGREEN}{track_metadata['ALBUM']}{bcolors.ENDC}" \
#                     f"from matching with {bcolors.OKCYAN}{row.ALBUM}{bcolors.ENDC}." \
#                     f"\n(A)dd album to whitelist as well." \
#                     f"\n(N)o, blacklist this title from future matches." \
#                     f"\n(O)pen the file to check" \
#                     f"\n(S)ave current changes and return to main menu." \
#                     f"\n(Q)uit to main menu & Discard all changes: "
#
#                 try:
#                     answer = input(message)[0].casefold()
#                 except IndexError:
#                     answer = None
#
#                 if answer == 'o':
#                     while answer == 'o':
#                         play_files_in_order(row.PATH)
#                         try:
#                             answer = input(message)[0].casefold()
#                         except IndexError:
#                             answer = None
#
#                 if answer == 'a' or answer == 'y':
#                     print(f"\n*** Ignoring Title ***")
#                     add_to_alt_title(db_row=row, track_metadata=track_metadata)
#                     # Force skip next section
#                     bypass_title = True
#                     if answer == 'a':
#                         # Explicitly this to force add album to whitelist in the next _if_ section
#                         bypass_album = True
#
#                 elif answer == 'q':
#                     return 99
#                 elif answer == 's':
#                     return 9
#                 elif answer == 'n':
#                     add_to_black_title(
#                         db_row=row, track_metadata=track_metadata)
#                 elif answer == 'b':
#                     query = Music.select().where(
#                         (Music.ALBUMARTIST == row.ALBUMARTIST) & (Music.ALBUM == row.ALBUM))
#                     for row2 in query:
#                         add_to_black_album(row2, track_metadata)
#                     pass
#                 else:
#                     print("Invalid input, skipping track.")
#                     continue
#
#             ##########################
#             # Album Matching section #
#             ##########################
#             if bypass_title or db_title == spotify_title or \
#                     is_title_in_alt_title(db_row=row, track_metadata=track_metadata):
#
#                 track_matches_spot_album, path_index = is_item_in_db_column_with_index(db_album,
#                                                                                         spotify_album)
#
#                 # We cannot use fuzz as we want to ensure the album is exactly the same or prompt the user!
#                 if track_matches_spot_album \
#                         or is_album_in_alt_album(db_row=row, track_metadata=track_metadata):
#                     """
#                     TODO: If there are multiple paths, use the path index corresponding to the matching Album index.
#                     For ex, spotify's "My Propeller" belongs to DB Albums [My Propeller, Humbug]
#                     So return the path corresponding to the matched album.
#                     Since they are the same track, it *probably* won't be queried again after its matched.
#                     """
#                     if path_index is not None:
#                         # ~Why a list? User might say yes to a track with multiple paths manually~
#                         # TAG: cd213e2f
#                         track_path = [str_to_list(row.PATH)[path_index]]
#                     else:
#                         track_path = str_to_list(row.PATH)
#                     result.append({
#                         'ALBUMARTIST': album_artist.ALBUMARTIST,
#                         'PATH': track_path,
#                         'ARTIST': str_to_list(row.ARTIST),
#                         'STREAMHASH': row.STREAMHASH
#                     })
#                 else:
#                     if is_item_in_db_column(row.blackALBUM, track_metadata['ALBUM']):
#                         # This track belongs to another existing album in the DB or we do not have it.
#                         # If subsequent iterations do not get this track then it will be a part of unmatched list.
#                         continue
#
#                     message = \
#                         f"\nSpotify URL: {track_metadata['SPOTIFY']}" \
#                         f"\nSpotify / DB Album:" \
#                         f"\n{bcolors.OKGREEN}" \
#                         f"{track_metadata['ALBUM']}{bcolors.ENDC} / {bcolors.OKCYAN}{row.ALBUM}" \
#                         f"{bcolors.ENDC}" \
#                         f"\n\nPATH {row.PATH}" \
#                         f"\n\nAre these the same?" \
#                         f"\n(Y)es, this is an alternate album." \
#                         f"\n(A)llow all tracks from this album to match Spotify's Album." \
#                         f"\n(B)lacklist {bcolors.OKGREEN}{track_metadata['ALBUM']}{bcolors.ENDC}" \
#                         f" from matching with {bcolors.OKCYAN}{row.ALBUM}{bcolors.ENDC} ever again." \
#                         f"\n(N)o, blacklist this Album from future matches." \
#                         f"\n(O)pen the file to check" \
#                         f"\n(S)ave current changes and return to main menu." \
#                         f"\n(Q)uit to main menu & Discard all changes: "
#
#                     message2 = str(f"\nSpotify URL: {track_metadata['SPOTIFY']}"
#                                     f"\nSpotify / DB Album:"
#                                     f"\n{bcolors.OKGREEN}"
#                                     f"{track_metadata['ALBUM']}{bcolors.ENDC} / {bcolors.OKCYAN}{row.ALBUM}"
#                                     f"{bcolors.ENDC}"
#                                     f"\n\nPATH {row.PATH}"
#                                     f"\nAre these the same?")
#
#                     message2 += "\n(Y)es, this is an alternate Album." \
#                                 "\n(A)llow all tracks from this album to match Spotify's Album." \
#                                 "\n(N)o, blacklist this Album from future matches." \
#                                 "\n(S)ave current changes and return to main menu." \
#                                 "\nDiscard all changes & (Q)uit to main menu: "
#
#                     try:
#                         if not bypass_album:
#                             answer = input(message)[0].casefold()
#                         else:
#                             answer = 'y'
#
#                     except IndexError:
#                         answer = None
#
#                     if answer == 'o':
#                         while answer == 'o':
#                             play_files_in_order(row.PATH)
#                             try:
#                                 answer = input(message)[0].casefold()
#                             except IndexError:
#                                 answer = None
#
#                     if answer == 'n' or answer == 'N':
#                         add_to_black_album(row, track_metadata)
#                         continue
#                     elif answer == 'b':
#                         query = Music.select().where(
#                             (Music.ALBUMARTIST == row.ALBUMARTIST) & (Music.ALBUM == row.ALBUM))
#                         for row2 in query:
#                             add_to_black_album(row2, track_metadata)
#                         pass
#                     if answer == 'y' or answer == 'a':
#                         if answer == 'a':
#                             query = Music.select().where(
#                                 (Music.ALBUMARTIST == row.ALBUMARTIST) & (Music.ALBUM == row.ALBUM))
#                             for row2 in query:
#                                 add_to_alt_album(row2, track_metadata)
#                         else:
#                             add_to_alt_album(row, track_metadata)
#                         result.append({
#                             'ALBUMARTIST': album_artist.ALBUMARTIST,
#                             'PATH': str_to_list(row.PATH),
#                             'ARTIST': str_to_list(row.ARTIST),
#                             'STREAMHASH': row.STREAMHASH
#                         })
#                     elif answer == 's':
#                         return 9
#                     elif answer == 'q':
#                         return 99
#                     else:
#                         print("Invalid input, skipping track.")
#                         continue
#                 # if spotify_album_artist not in result.keys():
#                 #     result[spotify_album_artist] = []
#                 #
#                 # result[spotify_album_artist].append({
#                 #     'PATH': str_to_list(row.PATH),
#                 #     'STREAMHASH': row.STREAMHASH
#                 # })
#
#     """
#     If there's multiple matches, there is a chance that we are searching for a compilation album like
#     "The Metallica Blacklist" that contains tracks from various artists under the same Album Artist.
#     In these cases, try to see if the if the artists in the DB match spotify metadata.
#         - If there's a list of artists for a track in the DB, this list should be a subset of
#         Spotify track metadata as well. (And Vice Versa)
#         - If it's a single artist, it should match the first artist in Spotify track metadata.
#         TODO: There may be false positives!
#     """
#     if len(result) > 1:
#         trimmed_result = []
#         track_metadata_artist = [x.lower() for x in track_metadata['ARTIST']]
#         for item in result:
#             if isinstance(item['ARTIST'], list):
#
#                 # First Make the DB artist list case-insensitive!
#                 item['ARTIST'] = [x.lower() for x in item['ARTIST']]
#
#                 if set(item['ARTIST']).issubset(track_metadata_artist) or \
#                         set(track_metadata_artist).issubset(item['ARTIST']):
#
#                     trimmed_result.append(item)
#
#             else:
#                 if item['ARTIST'].lower() in track_metadata_artist:
#                     trimmed_result.append(item)
#         return trimmed_result
#
#     return result


def main():
    music_root_dir = os.path.expanduser("~/Music/Muzik")
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

    # =============== TODO: SEPARATE SPOTIFY INTEGRATION FILE NEEDED ===============
    # =============== TODO: For each unmatched result check for a whitelist file to resolve known false-negatives

    spot_playlist_tracks = spotify_fetch.main()

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

    print(f"{len(matched_list)}/{len(matched_list)+len(unmatched_list)} tracks Matched. ")

    with open("unmatched.json", "w") as jsonfile:
        jsonfile.write(json.dumps(unmatched_dict, indent=4, sort_keys=True))
    with open("matched.json", "w") as jsonfile:
        jsonfile.write(json.dumps(matched_dict, indent=4, sort_keys=True))

    db.close()
    master.close()
    #debug


if __name__ == '__main__':
    main()
