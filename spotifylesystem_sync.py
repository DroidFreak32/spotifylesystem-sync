from common import cls, missing_lrc
from db_ops import cleanup_db, sync_fs_to_db, export_altColumns, import_altColumns, partial_sync, \
    generate_local_playlist

import time

from spotify_ops import find_playlists_containing_tracks, generate_unsaved_track_playlists, dump_all_my_playlists

def action_generate_local_playlists():
    """
    Generates local equivalent of Spotify playlists.
    """
    skip_playlist_generation = False
    # if input(f"Enter Y to generate local and spotify playlists:").casefold() == 'y':
    #     skip_playlist_generation=False
    generate_local_playlist(
        all_saved_tracks=False,
        skip_playlist_generation=skip_playlist_generation
    )


def action_create_saved_tracks_playlist():
    """
    Generates a local playlist containing all saved/liked Spotify tracks.
    """
    # start = time.process_time()
    # for i in range(5):
    #     generate_local_playlist(all_saved_tracks=True, skip_playlist_generation=True)
    # print(f"\nTime: {time.process_time() - start}")
    generate_local_playlist(all_saved_tracks=True)


def action_generate_unsaved_playlist():
    """
    Generates a playlist of tracks that are present in user's playlists but are not saved to their library.
    Allows options to search only owned playlists, all playlists, and to merge results into a single playlist.
    """
    owner_only = True
    all_playlists = False
    merged = False

    if input("Enter Y to also search through playlists not owned by you:").casefold() == 'y':
        owner_only = False

    if input("Enter Y to scan ALL your playlists:").casefold() == 'y':
        all_playlists = True
        if input("Enter Y to merge ALL unsaved tracks to a single playlist:").casefold() == 'y':
            merged = True

    generate_unsaved_track_playlists(owner_only=owner_only,
                                     all_playlists=all_playlists,
                                     merge_all_unsaved_tracks=merged)


# MENU_OPTIONS is a list of tuples, where each tuple contains:
# 1. A string representing the menu option's description.
# 2. The function (or callable/lambda) to be executed when this option is selected.
MENU_OPTIONS = [
    ("Complete Sync filesystem to Local DB", sync_fs_to_db),
    ("Update modified files in DB", partial_sync),
    ("Generate spotify playlists locally", action_generate_local_playlists),
    ("Create a playlist of all saved spotify tracks", action_create_saved_tracks_playlist),
    ("Create a playlist of tracks without lrc files", missing_lrc),
    ("Generate playlist of tracks not saved to your library", action_generate_unsaved_playlist),
    # Use lambda to pass arguments to the function without executing it immediately
    ("Export all saved playlists in your profile", lambda: dump_all_my_playlists(owner_only=False)),
    ("Export owned playlists in your profile", lambda: dump_all_my_playlists(owner_only=True)),
    ("Export whitelist & blacklist", export_altColumns),
    ("Import whitelist & blacklist", import_altColumns),
    ("Cleanup duplicates in db", cleanup_db),
    ("Find your playlists containing a track via IDs", find_playlists_containing_tracks),
]


def menu():
    """
    Clears the console, displays the menu options, and prompts the user for their choice.
    """
    cls()
    for index, (description, _) in enumerate(MENU_OPTIONS, 1):
        print(f"{index}) {description}")
    print("Q - Quit")
    return input("Enter your choice: ")


def main():
    """
    Displays a menu of operations and executes the chosen action.
    """
    while True:
        choice = menu()
        if choice.casefold() == 'q':
            exit()

        if choice.isdigit():
            selection = int(choice)
            # Ensure selection is within valid bounds
            if 1 <= selection <= len(MENU_OPTIONS):
                cls()
                # Retrieve and execute the function from the tuple at the calculated index
                MENU_OPTIONS[selection - 1][1]()


if __name__ == '__main__':
    main()
    # start = time.process_time()
    # for i in range(4):
    #     generate_local_playlist(all_saved_tracks=True, skip_playlist_generation=True)
    # print(f"\nTime: {time.process_time() - start}")