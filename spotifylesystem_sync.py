from common import cls, missing_lrc
from db_ops import cleanup_db, sync_fs_to_db, export_altColumns, import_altColumns, partial_sync, \
    generate_local_playlist

import time

from spotify_ops import find_playlists_containing_tracks, generate_unsaved_track_playlists

print("outside common")


def menu():
    cls()
    menu_output = ("1) Complete Sync filesystem to Local DB\n"
                   "2) Update modified files in DB\n"
                   "3) Generate spotify playlists locally\n"
                   "4) Create a playlist of all saved spotify tracks\n"
                   "5) Create a playlist of tracks without lrc files\n"
                   "6) Export whitelist & blacklist\n"
                   "7) Import whitelist & blacklist\n"
                   "8) Cleanup duplicates in db\n"
                   "9) Find your playlists containing a track via IDs\n"
                   "10) Generate unsaved track playlist\n"
                   "Q - Quit\n"
                   "Enter your choice: ")
    choice = input(menu_output)
    return choice


def main():

    while True:
        choice = menu()
        if choice == '1':
            cls()
            sync_fs_to_db()
        elif choice == '2':
            cls()
            partial_sync()
        elif choice == '3':
            cls()
            generate_local_playlist(all_saved_tracks=False)
        elif choice == '4':
            cls()
            # start = time.process_time()
            # for i in range(5):
            #     generate_local_playlist(all_saved_tracks=True, skip_playlist_generation=True)
            # print(f"\nTime: {time.process_time() - start}")
            generate_local_playlist(all_saved_tracks=True)
        elif choice == '5':
            cls()
            missing_lrc()
        elif choice == '6':
            cls()
            export_altColumns()
        elif choice == '7':
            cls()
            import_altColumns()
        elif choice == '8':
            cls()
            cleanup_db()
        elif choice == '9':
            cls()
            find_playlists_containing_tracks()
        elif choice == '10':
            cls()
            generate_unsaved_track_playlists()
        elif choice.casefold() == 'q':
            exit()
        else:
            continue
        input("Press Enter key to continue")
    print("Received config")


if __name__ == '__main__':
    main()