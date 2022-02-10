import db_ops
import spotify_ops

from common import *



def menu():
    cls()
    menu_output = ("1) Complete Sync filesystem to Local DB\n"
                   "2) Update modified files in DB\n"
                   "3) Generate spotify playlists locally\n"
                   "4) Dump missing playlist tracks\n"
                   "Q - Quit\n"
                   "Enter your choice: ")
    choice = input(menu_output)
    return choice


def main():

    while True:
        choice = menu()
        if choice == '1':
            db_ops.complete_sync(find_flacs(music_root_dir), db_path)
        elif choice == '2':
            db_ops.partial_sync(find_flacs(music_root_dir), db_path)
        elif choice == '3':
            db_ops.generate_playlist()
        elif choice == '4':
            db_ops.generate_playlist()
        else:
            break
    print("Received config")


if __name__ == '__main__':
    main()
