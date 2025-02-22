import json
import os
import subprocess
from copy import deepcopy
from pathlib import Path
from pprint import pprint

from rapidfuzz import fuzz
from peewee import BlobField, Value
from peewee import CharField
from peewee import DoesNotExist
from peewee import ForeignKeyField
from peewee import IntegrityError
from peewee import Model
from peewee import TextField
from playhouse.sqlite_ext import CSqliteExtDatabase

import spotify_ops
from common import bcolors, fetch_metadata_in_background, generate_m3u, generate_metadata_with_warnings, get_last_flac_mtime, \
    list2dictmerge, music_root_dir, \
    db_path, db_mtime_marker, play_files_in_order, get_current_datetime, is_title_a_known_mismatch
from common import liststr_to_list, find_flacs

db = CSqliteExtDatabase(":memory:")


class BaseModel(Model):
    class Meta:
        # constraints = [SQL('PRIMARYKEY ("ALBUMARTIST" COLLATE NOCASE)')]
        database = db


class AlbumArtist(BaseModel):
    # collation=NOCASE seems to avoid duplicate artist names due to caps in verbs
    ALBUMARTIST = TextField(index=True, collation='NOCASE')


class Music(BaseModel):
    ALBUMARTIST = ForeignKeyField(AlbumArtist, backref="tracks")
    ARTIST = TextField(index=True)

    ALBUM = TextField(index=True)
    # List of alternate album names, usually from spotify
    altALBUM = TextField(null=True)
    # List of albums that is not present in the DB but the track exists on another Album
    blackALBUM = TextField(null=True, unindexed=True)

    TITLE = TextField(index=True)
    altTITLE = TextField(null=True)
    blackTITLE = TextField(null=True, unindexed=True)

    LYRICS = BlobField(unindexed=True, null=True)
    ISRC = TextField(null=True)
    STREAMHASH = CharField(max_length=32, unique=True)
    PATH = TextField(unindexed=True)
    # Track Spotify TRACK ID
    SPOTIFY_TID = TextField(null=True)


def is_item_in_db_column_with_index(db_tag=None, track_tag=None):
    """
    Checks if a particular tag is present on a given db column
    Handles cases where column may contain a list.
    """
    if db_tag is None:
        return False, None
    if isinstance(liststr_to_list(db_tag), list):
        db_tag = deepcopy(liststr_to_list(db_tag))
        index = 0
        for tag in db_tag:
            if tag.casefold() == track_tag.casefold():
                return True, index
            index += 1
    elif db_tag.casefold() == track_tag.casefold():
        return True, None
    return False, None


def is_item_in_db_column(db_tag=None, track_tag=None):
    return_item, _ = is_item_in_db_column_with_index(db_tag, track_tag)
    return return_item


def is_album_in_alt_album(db_row, track_metadata):
    """
    Separate this as it is always a list
    """
    if db_row.altALBUM is not None:
        for item in liststr_to_list(db_row.altALBUM):
            if item.casefold() == track_metadata['ALBUM'].casefold():
                return True

    return False


def is_title_in_alt_title(db_row, track_metadata):
    """
    Separate this as it is always a list
    """
    if db_row.altTITLE is not None:
        for item in liststr_to_list(db_row.altTITLE):
            if item.casefold() == track_metadata['TITLE'].casefold():
                return True

    return False


def add_to_alt_album(db_row, track_metadata):
    """
    Function to add to a whitelist column.
    """
    altALBUM_to_add = liststr_to_list(db_row.altALBUM)
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
    return


def add_to_alt_title(db_row, track_metadata):
    """
    Function to add to a whitelist column.
    """
    altTITLE_to_add = liststr_to_list(db_row.altTITLE)
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
    blackALBUM_to_add = liststr_to_list(db_row.blackALBUM)
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
    blackTITLE_to_add = liststr_to_list(db_row.blackTITLE)
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

def get_album_artist_from_merged_data(spotify_album_artist, spotify_playlist_tracks_merged):
    """
    Retrieves the AlbumArtist object from the database based on provided data,
    handling potential alternative album artists.
    Example: SOAD - Steal this Album!

    Args:
        spotify_album_artist: The primary album artist from Spotify.
        spotify_playlist_tracks_merged: Dictionary containing track data, including potential 'alt_ALBUMARTISTS'.

    Returns:
        The matching AlbumArtist object from the database.

    Raises:
        DoesNotExist: If no matching album artist is found in the database.
    """
    def f7(seq):
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]

    artists_list = []

    try:
        artists_list.append(AlbumArtist.get(AlbumArtist.ALBUMARTIST == spotify_album_artist))
    except DoesNotExist:
        try:
            artists_list.append(AlbumArtist.get(AlbumArtist.ALBUMARTIST == spotify_album_artist.casefold()))
        except DoesNotExist:
            if spotify_playlist_tracks_merged[spotify_album_artist][0].get('alt_ALBUMARTISTS'):
                for alt_artist in spotify_playlist_tracks_merged[spotify_album_artist][0].get('alt_ALBUMARTISTS'):
                    try:
                        artists_list.append(AlbumArtist.get(AlbumArtist.ALBUMARTIST == alt_artist))
                    except DoesNotExist:
                        try:
                           artists_list.append(AlbumArtist.get(AlbumArtist.ALBUMARTIST == alt_artist.casefold()))
                        except DoesNotExist:
                            pass  # Continue to the next alt_artist if not found
    if spotify_playlist_tracks_merged[spotify_album_artist][0].get('ARTIST'):
        for alt_artist in spotify_playlist_tracks_merged[spotify_album_artist][0].get('ARTIST'):
            try:
                artists_list.append(AlbumArtist.get(AlbumArtist.ALBUMARTIST == alt_artist))
            except DoesNotExist:
                try:
                    artists_list.append(AlbumArtist.get(AlbumArtist.ALBUMARTIST == alt_artist.casefold()))
                except DoesNotExist:
                    pass  # Continue to the next alt_artist if not found
    if len(artists_list) > 0:
        return f7(artists_list)
    else:
        # If none of the above attempts succeed, raise DoesNotExist
        raise DoesNotExist("No matching AlbumArtist found.")

def search_track_in_db(track_metadata=None, album_artists=None):
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

    album_artist_tracks = None
    result = []
    spotify_title = deepcopy(track_metadata['TITLE'].casefold())
    spotify_album = deepcopy(track_metadata['ALBUM'].casefold())
    spotify_tid = deepcopy(track_metadata['SPOTIFY_TID'])
    spotify_linked_tid = deepcopy(track_metadata['SPOTIFY_LINKED_TID'])
    db_track_contains_tid = False

    def safe_title_substring(_db_title='test', _spotify_title='test'):
        """
        On many cases the title we need is already a substring of Spotify's title
        This function matches these, without too many false positive matches on shorter titles.
        10 characters matching should be a good sweet spot to avoid false positives like
        Ex: "AbcArtist - SHORT.flac" should not match "AbcArtist - This is not a SHORTER title.flac"
        """
        if len(_db_title) > 10 and _db_title.casefold() in _spotify_title.casefold():
            return True
        return False

    def check_live_tracks_mismatch(_db_title='test', _spotify_title='test'):
        if ('live' in _db_title) or ('live' in _spotify_title):
            if ('live' in _db_title) and ('live' in _spotify_title):
                return False
            else:
                return True
        return False


    """
    Update: Search in 2 stages - 1st attempt to match Album, else browse through all files.
    """

    for album_artist in album_artists:
        stage = 0
        while stage < 2:
            if stage == 0:
                # Stage 1 - Match only tracks with similar Album name
                # https://stackoverflow.com/questions/74090945
                # Either spotify_album matches db_album or is dbAlbum is a substring OR spotify_album is in altALBUM
                # Stage 2: All the rest of the tracks
                #  Note to self: Do not think of first filtering blacklists in PeeWee Queries as blacklists are stored as
                #  lists. If spotify_album is a substring of blackALBUM but matches ALBUM, the filter will remove this
                #  row!
                # album_artist_tracks = Music.select().where( (Music.ALBUMARTIST == album_artist) & (Music.ALBUM ** spotify_album))

                # Try to match existing Spotify TIDs first to reduce future prompts.
                # album_artist_tracks = Music.select().where(
                #     (Music.ALBUMARTIST == album_artist) & (Music.SPOTIFY_TID.contains(spotify_tid))
                # )

                album_artist_tracks = Music.select().where(
                    (Music.SPOTIFY_TID.contains(spotify_tid)) | (Music.SPOTIFY_TID.contains(spotify_linked_tid))
                )

                if len(album_artist_tracks) >= 1:
                    db_track_contains_tid = True


                else:
                    # THIS DOES NOT WORK:
                    # peewee.OperationalError: sub-select returns 14 columns - expected 1
                    #
                    # album_artist_tracks = album_artist.tracks.select(Music).where(
                    #     ((Music.ALBUM ** track_metadata['ALBUM']) | Music.altALBUM.contains(track_metadata['ALBUM']))
                    # )
                    # if len(album_artist_tracks) == 0:
                    #     album_artist_tracks = album_artist.tracks.select(Music).where(
                    #         (Value(track_metadata['ALBUM']).contains(Music.ALBUM))
                    #     )

                    album_artist_tracks = Music.select().where(
                        (Music.ALBUMARTIST == album_artist) &
                        ((Music.ALBUM ** track_metadata['ALBUM']) | Music.altALBUM.contains(track_metadata['ALBUM']))
                    )
                    if len(album_artist_tracks) == 0:
                        album_artist_tracks = Music.select().where(
                            (Music.ALBUMARTIST == album_artist) & (Value(track_metadata['ALBUM']).contains(Music.ALBUM))
                        )

            else:
                # continue
                # Skips tracks from stage 1
                album_artist_tracks = album_artist.tracks.select(Music).where(Music.id.not_in(album_artist_tracks))
                db_track_contains_tid = False
                # album_artist_tracks = album_artist.tracks

            for row in album_artist_tracks:
                # Reset these flags in each iteration
                bypass_title = False
                bypass_album = False

                db_title = deepcopy(row.TITLE.casefold())

                db_album = deepcopy(row.ALBUM.casefold())

                if fuzz.ratio(db_title, spotify_title) >= 85 \
                        or is_title_in_alt_title(db_row=row, track_metadata=track_metadata) \
                        or spotify_title == db_title or safe_title_substring(db_title, spotify_title) \
                        or is_title_a_known_mismatch(db_title, spotify_title):
                    # For ex "The Diary of Jane" is in "The Diary of Jane - Single Version" so match such cases too.

                    if check_live_tracks_mismatch(db_title, spotify_title) \
                            and not is_title_in_alt_title(db_row=row, track_metadata=track_metadata):
                        # If the track is a live version but the DB doesn't contain that string, unmatch immediately.
                        # Skips unnecessary matches of live versions with studio versions
                        continue

                    if is_item_in_db_column(row.blackTITLE, track_metadata['TITLE']):
                        # This track is probably another edition, i.e. Acoustic Version
                        # If subsequent iterations do not get this track then it will be a part of unmatched list.
                        continue

                    if is_item_in_db_column(row.blackALBUM, track_metadata['ALBUM']):
                        # This track belongs to another existing album in the DB, or we do not have it.
                        # If subsequent iterations do not get this track then it will be a part of unmatched list.
                        continue
                    if db_title != spotify_title and not is_title_in_alt_title(db_row=row, track_metadata=track_metadata):
                        """
                        We don't have an exact match, so prompt user to verify and update alternate / blacklist tags in DB.
                        """
                        message = \
                            f"\nSpotify URL: {track_metadata['SPOTIFY']}" \
                            f"\nSpotify / DB Title:" \
                            f"\n{bcolors.OKGREEN}" \
                            f"{track_metadata['TITLE']}{bcolors.ENDC} / {bcolors.OKCYAN}{row.TITLE}" \
                            f"{bcolors.ENDC}" \
                            f"\n\nPATH {row.PATH}" \
                            f"\n\nAre these the same?" \
                            f"\n(Y)es, this is an alternate title." \
                            f"\n(B)lacklist {bcolors.OKGREEN}{track_metadata['ALBUM']}{bcolors.ENDC}" \
                            f" from matching with {bcolors.OKCYAN}{row.ALBUM}{bcolors.ENDC}." \
                            f"\n(A)dd album to whitelist as well." \
                            f"\n(N)o, blacklist this title from future matches." \
                            f"\n(O)pen the file to check" \
                            f"\n(S)ave current changes and return to main menu." \
                            f"\n(Q)uit to main menu & Discard all changes: "

                        try:
                            answer = input(message)[0].casefold()
                        except IndexError:
                            answer = None

                        if answer == 'o':
                            while answer == 'o':
                                play_files_in_order(row.PATH)
                                try:
                                    answer = input(message)[0].casefold()
                                except IndexError:
                                    answer = None

                        if answer == 'a' or answer == 'y':
                            print(f"\n*** Ignoring Title ***")
                            add_to_alt_title(db_row=row, track_metadata=track_metadata)
                            # Force skip next section
                            bypass_title = True
                            if answer == 'a':
                                # Explicitly this to force add album to whitelist in the next _if_ section
                                bypass_album = True

                        elif answer == 'q':
                            return 99
                        elif answer == 's':
                            return 9
                        elif answer == 'n':
                            add_to_black_title(
                                db_row=row, track_metadata=track_metadata)
                        elif answer == 'b':
                            query = Music.select().where(
                                (Music.ALBUMARTIST == row.ALBUMARTIST) & (Music.ALBUM == row.ALBUM))
                            for row2 in query:
                                add_to_black_album(row2, track_metadata)
                            pass
                        else:
                            print("Invalid input, skipping track.")
                            continue

                    ##########################
                    # Album Matching section #
                    ##########################
                    if bypass_title or db_title == spotify_title or \
                            is_title_in_alt_title(db_row=row, track_metadata=track_metadata):

                        track_matches_spot_album, path_index = is_item_in_db_column_with_index(db_album,
                                                                                            spotify_album)

                        # We cannot use fuzz as we want to ensure the album is exactly the same or prompt the user!
                        if track_matches_spot_album \
                                or is_album_in_alt_album(db_row=row, track_metadata=track_metadata):
                            """
                            TODO: If there are multiple paths, use the path index corresponding to the matching Album index.
                            For ex, spotify's "My Propeller" belongs to DB Albums [My Propeller, Humbug]
                            So return the path corresponding to the matched album.
                            Since they are the same track, it *probably* won't be queried again after its matched.
                            """
                            if path_index is not None:
                                # ~Why a list? User might say yes to a track with multiple paths manually~
                                # TAG: cd213e2f
                                track_path = [liststr_to_list(row.PATH)[path_index]]
                            else:
                                track_path = liststr_to_list(row.PATH)

                            if db_track_contains_tid:
                                db_tids = liststr_to_list(row.SPOTIFY_TID)
                                if db_tids is not None:
                                    db_tids.sort()
                                unique_tids = sorted(
                                    set([spotify_tid, spotify_linked_tid] + db_tids)
                                )
                                if len(unique_tids) == len(db_tids):
                                    skip_db_update = True
                                    # PROFILE THIS!! MAY NOT BE NEEDED
                                    if db_tids != unique_tids:
                                        pass
                                else:
                                    update_trackid_in_db(spotify_tid=unique_tids, streamhash=row.STREAMHASH,
                                                        existing_tid=row.SPOTIFY_TID)
                            else:
                                unique_tids = sorted(
                                    {spotify_tid, spotify_linked_tid}
                                )
                                update_trackid_in_db(spotify_tid=unique_tids, streamhash=row.STREAMHASH,
                                                    existing_tid=row.SPOTIFY_TID)

                            result.append({
                                'ALBUMARTIST': album_artist.ALBUMARTIST,
                                'PATH': track_path,
                                'ARTIST': liststr_to_list(row.ARTIST),
                                'SPOTIFY_TID': unique_tids,
                                'STREAMHASH': row.STREAMHASH,
                            })

                        else:
                            if is_item_in_db_column(row.blackALBUM, track_metadata['ALBUM']):
                                # This track belongs to another existing album in the DB or we do not have it.
                                # If subsequent iterations do not get this track then it will be a part of unmatched list.
                                continue

                            message = \
                                f"\nSpotify URL: {track_metadata['SPOTIFY']}" \
                                f"\nSpotify / DB Album:" \
                                f"\n{bcolors.OKGREEN}" \
                                f"{track_metadata['ALBUM']}{bcolors.ENDC} / {bcolors.OKCYAN}{row.ALBUM}" \
                                f"{bcolors.ENDC}" \
                                f"\n\nPATH {row.PATH}" \
                                f"\n\nAre these the same?" \
                                f"\n(Y)es, this is an alternate album." \
                                f"\n(A)llow all tracks from this album to match Spotify's Album." \
                                f"\n(B)lacklist {bcolors.OKGREEN}{track_metadata['ALBUM']}{bcolors.ENDC}" \
                                f" from matching with {bcolors.OKCYAN}{row.ALBUM}{bcolors.ENDC} ever again." \
                                f"\n(N)o, blacklist this Album from future matches." \
                                f"\n(O)pen the file to check" \
                                f"\n(S)ave current changes and return to main menu." \
                                f"\n(Q)uit to main menu & Discard all changes." \
                                f"\nOr skip this track by pressing enter: "
                            message2 = str(f"\nSpotify URL: {track_metadata['SPOTIFY']}"
                                        f"\nSpotify / DB Album:"
                                        f"\n{bcolors.OKGREEN}"
                                        f"{track_metadata['ALBUM']}{bcolors.ENDC} / {bcolors.OKCYAN}{row.ALBUM}"
                                        f"{bcolors.ENDC}"
                                        f"\n\nPATH {row.PATH}"
                                        f"\nAre these the same?")

                            message2 += "\n(Y)es, this is an alternate Album." \
                                        "\n(A)llow all tracks from this album to match Spotify's Album." \
                                        "\n(N)o, blacklist this Album from future matches." \
                                        "\n(S)ave current changes and return to main menu." \
                                        "\nDiscard all changes & (Q)uit to main menu: "

                            try:
                                if not bypass_album:
                                    answer = input(message)[0].casefold()
                                else:
                                    answer = 'y'

                            except IndexError:
                                answer = None

                            if answer == 'o':
                                while answer == 'o':
                                    play_files_in_order(row.PATH)
                                    try:
                                        answer = input(message)[0].casefold()
                                    except IndexError:
                                        answer = None

                            if answer == 'n' or answer == 'N':
                                add_to_black_album(row, track_metadata)
                                continue
                            elif answer == 'b':
                                query = Music.select().where(
                                    (Music.ALBUMARTIST == row.ALBUMARTIST) & (Music.ALBUM == row.ALBUM))
                                for row2 in query:
                                    add_to_black_album(row2, track_metadata)
                                pass
                            if answer == 'y' or answer == 'a':
                                if answer == 'a':
                                    query = Music.select().where(
                                        (Music.ALBUMARTIST == row.ALBUMARTIST) & (Music.ALBUM == row.ALBUM))
                                    for row2 in query:
                                        add_to_alt_album(row2, track_metadata)
                                else:
                                    add_to_alt_album(row, track_metadata)

                                if db_track_contains_tid:
                                    db_tids = liststr_to_list(row.SPOTIFY_TID)
                                    db_tids.sort()
                                    unique_tids = sorted(
                                        set([spotify_tid, spotify_linked_tid] + db_tids)
                                    )
                                    if len(unique_tids) == len(db_tids):
                                        skip_db_update = True
                                        # PROFILE THIS!! MAY NOT BE NEEDED
                                        if db_tids != unique_tids:
                                            pass
                                    else:
                                        update_trackid_in_db(spotify_tid=unique_tids, streamhash=row.STREAMHASH,
                                                            existing_tid=row.SPOTIFY_TID)
                                else:
                                    unique_tids = sorted(
                                        {spotify_tid, spotify_linked_tid}
                                    )
                                    update_trackid_in_db(spotify_tid=unique_tids, streamhash=row.STREAMHASH,
                                                        existing_tid=row.SPOTIFY_TID)

                                result.append({
                                    'ALBUMARTIST': album_artist.ALBUMARTIST,
                                    'PATH': liststr_to_list(row.PATH),
                                    'ARTIST': liststr_to_list(row.ARTIST),
                                    'SPOTIFY_TID': unique_tids,
                                    'STREAMHASH': row.STREAMHASH,
                                })
                            elif answer == 's':
                                return 9
                            elif answer == 'q':
                                return 99
                            else:
                                print("Invalid input, skipping track.")
                                continue
                        # if spotify_album_artist not in result.keys():
                        #     result[spotify_album_artist] = []
                        #
                        # result[spotify_album_artist].append({
                        #     'PATH': str_to_list(row.PATH),
                        #     'STREAMHASH': row.STREAMHASH
                        # })

            """
            If there's multiple matches, there is a chance that we are searching for a compilation album like
            "The Metallica Blacklist" that contains tracks from various artists under the same Album Artist.
            In these cases, try to see if the if the artists in the DB match spotify metadata.
            - If there's a list of artists for a track in the DB, this list should be a subset of
                Spotify track metadata as well. (And Vice Versa)
            - If it's a single artist, it should match the first artist in Spotify track metadata.
            TODO: There may be false positives!
            """
            if len(result) > 1:
                trimmed_result = []
                track_metadata_artist = [x.lower() for x in track_metadata['ARTIST']]
                for item in result:
                    if isinstance(item['ARTIST'], list):

                        # First Make the DB artist list case-insensitive!
                        item['ARTIST'] = [x.lower() for x in item['ARTIST']]

                        if set(item['ARTIST']).issubset(track_metadata_artist) or \
                                set(track_metadata_artist).issubset(item['ARTIST']):

                            trimmed_result.append(item)

                    else:
                        if item['ARTIST'].lower() in track_metadata_artist:
                            trimmed_result.append(item)
                return trimmed_result

            elif len(result) == 0:
                stage += 1
            else:
                return result
    return result


def dump_to_db(metadata):
    music_db_orm = None
    for album_artists, track_list in metadata.items():
        for track in track_list:
            """
            Get an AlbumArtist object, maybe for backref?? Blind copy pasta
            """
            try:
                # Avoids duplicates if artist already exists
                album_artist = AlbumArtist.get(
                    AlbumArtist.ALBUMARTIST == album_artists)
            except DoesNotExist:
                AlbumArtist.create(ALBUMARTIST=album_artists)
                album_artist = AlbumArtist.get(
                    AlbumArtist.ALBUMARTIST == album_artists)
            try:
                music_db_orm = Music.create(ALBUMARTIST=album_artist, ARTIST=track['ARTIST'], ALBUM=track['ALBUM'],
                                            altALBUM=None, blackALBUM=None,
                                            TITLE=track['TITLE'], altTITLE=None, blackTITLE=None,
                                            LYRICS=track['LYRICS'],
                                            ISRC=track['ISRC'],
                                            STREAMHASH=track['STREAMHASH'], SPOTIFY_TID=None,
                                            PATH=track['PATH'])
                music_db_orm.save()
            except IntegrityError:
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

                    if isinstance(liststr_to_list(row['PATH']), list):
                        multi_path = liststr_to_list(row['PATH'])
                        multi_path.append(track['PATH'])
                    else:
                        multi_path.append(row['PATH'])
                        multi_path.append(track['PATH'])
                    if isinstance(liststr_to_list(row['ALBUM']), list):
                        multi_album = liststr_to_list(row['ALBUM'])
                        multi_album.append(track['ALBUM'])
                    elif track['ALBUM'] == row['ALBUM']:
                        print(
                            f"{bcolors.WARNING}Is this file a duplicate copy?{bcolors.ENDC}\n")
                        multi_album = track['ALBUM']
                    else:
                        multi_album.append(row['ALBUM'])
                        multi_album.append(track['ALBUM'])
                    # print(multi_path)
                    query = Music.update(ALBUMARTIST=album_artist, ARTIST=track['ARTIST'], ALBUM=multi_album,
                                         altALBUM=row['altALBUM'], blackALBUM=row['blackALBUM'],
                                         TITLE=track['TITLE'], altTITLE=row['altTITLE'], blackTITLE=row['blackTITLE'],
                                         LYRICS=track['LYRICS'], ISRC=track['ISRC'], SPOTIFY_TID=row['SPOTIFY_TID'],
                                         PATH=multi_path).where(Music.STREAMHASH == track["STREAMHASH"])
                    query.execute()
                print(
                    f"Previous file: {multi_path[0]}\nCurrent file: {multi_path[1]}{bcolors.ENDC}")

    if music_db_orm is not None:
        music_db_orm.save()


def sync_fs_to_db(force_resync=True, flac_files=None, last_flac_mtime=1):
    master = CSqliteExtDatabase(db_path)

    # Prevent scanning for flac files on startup
    if flac_files is None:
        flac_files = find_flacs(music_root_dir)
    try:
        """
        TODO: Test this. Using this for now to prevent crashes on a fresh setup without db created
        """
        master.backup(db)
    except:
        master.create_tables([AlbumArtist, Music])
        master.commit()
        master.backup(db)
    if force_resync:
        # Rescan again to avoid crash when file is deleted while running this program
        flac_files = find_flacs(music_root_dir)
        last_flac_mtime = get_last_flac_mtime(flac_files)
        db.drop_tables([AlbumArtist, Music])
        db.create_tables([AlbumArtist, Music])

    metadata, warning_flag = generate_metadata_with_warnings(music_root_dir, flac_files)
    if warning_flag:
        answer = input("\nIf there are warnings above, for example - Multiple Album Artist tag in a file " +
                       "\nstop this program and fix them. Else, type F to ignore the warnings and continue.")
        if answer == 'F' or answer == 'f':
            answer = input("Are you really sure you want to ignore the warnings? (Y/N)")
            if answer == 'Y' or answer == 'y':
                warning_flag = False

    # User agrees to continue
    if not warning_flag:
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
    # read the last modified time from marker
    with open(db_mtime_marker) as f:
        db_mtime = float(f.readline().strip())
    last_flac_mtime = get_last_flac_mtime(flac_files)
    for flac_file in flac_files:
        if db_mtime < os.path.getmtime(os.path.join(music_root_dir, flac_file)):
            new_files.append(flac_file)
    if len(new_files) == 0:
        print(f"No new files exist.")
        return
    print(f"New files:\n_________")
    new_files.sort()
    # pprint(new_files)
    for i in range(len(new_files)):
        print(f"{i+1}. {new_files[i]}")
    input("Press enter to continue..")
    if len(new_files) > 0:
        sync_fs_to_db(force_resync=False, flac_files=new_files,
                      last_flac_mtime=last_flac_mtime)
    cleanup_db()


def update_trackid_in_db(spotify_tid=None, streamhash=None, existing_tid=None):
    if existing_tid is None:
        tid_to_add = spotify_tid
    else:
        tid_to_add = sorted(set(
            spotify_tid + liststr_to_list(existing_tid)
        ))
    # else:
    # All checks passed so update the DB
    query = Music.update(SPOTIFY_TID=tid_to_add).where(Music.STREAMHASH == streamhash)
    query.execute()


def generate_local_playlist(all_saved_tracks=False, skip_playlist_generation=False):

    """
    TODO: Parallelize DB searching by adding a flag to bypass any user prompts and just store all the SUCCESS results
            then strip these tracks and redo the classic brute-force searching which then asks for prompts.
            For large number of songs of the artist, this method could be used:
    album_artist = AlbumArtist.get(...)
    fast_result = a_pool.starmap(search_track_in_db, zip(spotify_playlist_tracks_merged['Arctic Monkeys'], repeat(album_artist)))
    """
    # Flags to quit generating playlists.
    skip_generation_and_save = False
    abort_abort = False

    # Copy DB in memory to avoid mistakes being reflected into the main DB.
    master = CSqliteExtDatabase(db_path)
    master.backup(db)
    if not all_saved_tracks:
        spotify_playlist_name, spotify_playlist_tracks = spotify_ops.fetch_playlist_tracks(owner_only=True)
    else:
        # spotify_playlist_name, spotify_playlist_tracks = spotify_ops.get_my_saved_tracks()
        # with open("allmytracks.json", "w") as jsonfile:
        #     jsonfile.write(json.dumps(deepcopy(spotify_playlist_tracks), indent=4, sort_keys=False))
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
    for spotify_album_artist, _ in spotify_playlist_tracks_merged.items():
        try:
            album_artists = get_album_artist_from_merged_data(spotify_album_artist, spotify_playlist_tracks_merged)
        except DoesNotExist:
            # try:
            #     # Maybe some casing is different
            #     album_artist = AlbumArtist.get(
            #         AlbumArtist.ALBUMARTIST == spotify_album_artist.casefold())
            # except DoesNotExist:
                print(f"Artist: {spotify_album_artist} does not exist")
                # Add all tracks of this artist to unmatched tracks and increase offset accordingly
                skipped_tracks = []
                for track in spotify_playlist_tracks_merged[spotify_album_artist]:
                    skipped_tracks.append(
                        {'ALBUMARTIST': spotify_album_artist} | track
                    )

                    if track['SPOTIFY_TID'] != track['SPOTIFY_LINKED_TID']:
                        unmatched_track_ids.append(spotify_ops.return_saved_tid(
                            [track['SPOTIFY_TID'], track['SPOTIFY_LINKED_TID']]
                        ))
                    else:
                        unmatched_track_ids.append(track['SPOTIFY_TID'])

                unmatched_list += skipped_tracks
                offset += len(skipped_tracks)
                continue

        for playlist_track in spotify_playlist_tracks_merged[spotify_album_artist]:
            skip_generation_and_save = False
            abort_abort = False
            offset += 1
            print(
                f"Querying DB for tracks: {offset} / {spotify_playlist_track_total}", end="\r")

            result = \
                search_track_in_db(track_metadata=playlist_track, album_artists=album_artists)
            if result == 9:
                skip_generation_and_save = True
                break
            elif result == 99:
                abort_abort = True
                break
            if len(result) > 1:
                print(
                    f"{bcolors.FAIL}Multiple Matches found: {result}{bcolors.ENDC}")
                # TODO: Ask user for correct match by checking playlist_track['SPOTIFY']
                continue
            elif len(result) == 0:
                unmatched_track = {'ALBUMARTIST': spotify_album_artist} | playlist_track
                unmatched_list.append(unmatched_track)
                if unmatched_track['SPOTIFY_TID'] != unmatched_track['SPOTIFY_LINKED_TID']:
                    unmatched_track_ids.append(spotify_ops.return_saved_tid(
                        [unmatched_track['SPOTIFY_TID'], unmatched_track['SPOTIFY_LINKED_TID']]
                    ))
                else:
                    unmatched_track_ids.append(unmatched_track['SPOTIFY_TID'])
                # print(f"No result found for {playlist_track['ALBUMARTIST']} - {playlist_track['TITLE']}")
                continue
            matched_list += result
            if isinstance(liststr_to_list(result[0]['PATH']), list):
                # Use the 1st PATH. TODO: Make this more accurate by checking Album
                # TAG: cd213e2f
                result[0]['PATH'] = result[0]['PATH'][0]
            matched_paths.append(result[0]['PATH'])
        if abort_abort:
            print(f"{bcolors.WARNING}Aborting!{bcolors.ENDC}")
            return
        elif skip_generation_and_save:
            break

    # for item in matched_list:
    #     update_trackid_in_db(spotify_tid=item['SPOTIFY_TID'], streamhash=item['STREAMHASH'])
    unmatched_dict = list2dictmerge(deepcopy(unmatched_list))
    matched_dict = list2dictmerge(deepcopy(matched_list))
    print(f"\n{len(matched_list)}/{spotify_playlist_track_total} tracks Matched. ")

    if not skip_playlist_generation:
        if input("Do you want to generate an m3u file for the matched songs?\nY/N: ")[0].casefold() == 'y':
            generate_m3u(playlist_name=spotify_playlist_name, track_paths=matched_paths)
        if len(unmatched_track_ids) > 0:
            if input("Do you want to generate a new spotify playlist "
                     "for the UNMATCHED songs?\nY/N: ")[0].casefold() == 'y':
                spotify_ops.generate_playlist_from_tracks(track_ids=unmatched_track_ids,
                                                          playlist_name=spotify_playlist_name)

    with open("unmatched.json", "w") as jsonfile:
        encoded_json = json.dumps(unmatched_dict, indent=4, sort_keys=True, ensure_ascii=False)
        jsonfile.write(encoded_json)
    with open("matched.json", "w") as jsonfile:
        encoded_json = json.dumps(matched_dict, indent=4, sort_keys=True, ensure_ascii=False)
        jsonfile.write(encoded_json)

    db.backup(master)
    master.execute_sql('VACUUM;')

def export_altColumns():
    master = CSqliteExtDatabase(db_path)
    master.backup(db)
    alt_columns = []
    tracks = Music.select().where(
        Music.altALBUM.is_null(False) | Music.altTITLE.is_null(False) | Music.blackALBUM.is_null(
            False) | Music.blackTITLE.is_null(False)).order_by(Music.STREAMHASH)
    for row in tracks:
        alt_columns.append(
            {
                'STREAMHASH': row.STREAMHASH,
                'altALBUM': liststr_to_list(row.altALBUM),
                'blackALBUM': liststr_to_list(row.blackALBUM),
                'altTITLE': liststr_to_list(row.altTITLE),
                'blackTITLE': liststr_to_list(row.blackTITLE),
                'SPOTIFY_TID': liststr_to_list(row.SPOTIFY_TID)
            }
        )

    filename = f"altColumns_{get_current_datetime()}.json"
    with open(filename, "w") as jsonfile:
        jsonfile.write(json.dumps(alt_columns, indent=2, sort_keys=False))
    print(f"Whitelist & Blacklist exported to: {os.path.join(os.getcwd(), filename)}")
    db.backup(master)
    master.execute_sql('VACUUM;')


def import_altColumns():
    master = CSqliteExtDatabase(db_path)
    master.backup(db)

    answer = input(f"Enter the name of alt_columns.json file: ")
    if os.path.exists(os.path.join(os.getcwd(), answer)):
        json_file_path = os.path.join(os.getcwd(), answer)
    else:
        json_file_path = 'altColumns.json'
    print(f"Reading {json_file_path}")
    with open(json_file_path, 'r') as j:
        altColumn = json.loads(j.read())

    for item in altColumn:
        query = Music.update(
            altALBUM=item['altALBUM'], blackALBUM=item['blackALBUM'],
            altTITLE=item['altTITLE'], blackTITLE=item['blackTITLE'], SPOTIFY_TID=item['SPOTIFY_TID']
        ).where(Music.STREAMHASH == item['STREAMHASH'])
        query.execute()

    db.backup(master)
    master.execute_sql('VACUUM;')


def cleanup_db():
    master = CSqliteExtDatabase(db_path)
    master.backup(db)
    deleted_files = []
    query = Music.select()
    total_tracks = Music.select().__len__()
    # total_tracks = Music.select().count() now gives error
    count = 0
    for row in query:
        db_ALBUMARTIST = row.ALBUMARTIST
        db_ARTIST = liststr_to_list(row.ARTIST)
        db_ALBUM = liststr_to_list(row.ALBUM)
        db_altALBUM = liststr_to_list(row.altALBUM)
        db_blackALBUM = liststr_to_list(row.blackALBUM)
        db_TITLE = row.TITLE
        db_altTITLE = liststr_to_list(row.altTITLE)
        db_blackTITLE = liststr_to_list(row.blackTITLE)
        db_LYRICS = row.LYRICS
        db_ISRC = row.ISRC
        db_SPOTIFY_TID = liststr_to_list(row.SPOTIFY_TID)
        db_STREAMHASH = row.STREAMHASH
        db_PATH = liststr_to_list(row.PATH)

        # Remove duplicate / non-existent paths
        if isinstance(db_PATH, list):
            # If the paths are a list, the same track is present on multiple locations
            new_paths = []
            for path in list(set(db_PATH)):
                if os.path.exists(os.path.join(music_root_dir, path)):
                    new_paths.append(path)
            if len(new_paths) == 1:
                db_PATH = new_paths[0]
            else:
                db_PATH = new_paths
        else:
            # There is just one copy of the file.
            # If this one copy doesn't exist, delete the entire row.
            if not os.path.exists(os.path.join(music_root_dir, db_PATH)):
                deleted_files.append(db_PATH)
                # https://docs.peewee-orm.com/en/latest/peewee/api.html#Model.delete_instance
                row.delete_instance()
                count += 1
                print(f"{bcolors.WARNING}The track {db_PATH} no longer exists!{bcolors.ENDC}")
                print(f"Cleaned {count}/{total_tracks} rows", end="\r")
                db.backup(master)
                master.execute_sql('VACUUM;')
                continue

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

        # These are always List items.
        # https://stackoverflow.com/a/7961390/6437140
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
        if db_SPOTIFY_TID is not None:
            db_SPOTIFY_TID = list(set(db_SPOTIFY_TID))
            if len(db_SPOTIFY_TID) == 0:
                db_SPOTIFY_TID = None

        update_query = Music.update(ALBUM=db_ALBUM, altALBUM=db_altALBUM, blackALBUM=db_blackALBUM,
                                    altTITLE=db_altTITLE,
                                    blackTITLE=db_blackTITLE,
                                    SPOTIFY_TID=db_SPOTIFY_TID, PATH=db_PATH).where(Music.STREAMHASH == db_STREAMHASH)
        update_query.execute()
        count += 1
        print(f"Cleaned {count}/{total_tracks} rows", end="\r")

    db.backup(master)
    master.execute_sql('VACUUM;')


if __name__ == '__main__':
    import spotifylesystem_sync

    spotifylesystem_sync.main()
# else:
#     input("\nPress enter to go back to the main menu")
