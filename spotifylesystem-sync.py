from db_ops import sync_fs_to_db, export_altColumns, import_altColumns, partial_sync, generate_playlist

from common import cls
print("outside common")


def menu():
    cls()
    menu_output = ("1) Complete Sync filesystem to Local DB\n"
                   "2) Update modified files in DB\n"
                   "3) Generate spotify playlists locally\n"
                   "4) Export whitelist & blacklist\n"
                   "5) Import whitelist & blacklist\n"
                   "Q - Quit\n"
                   "Enter your choice: ")
    choice = input(menu_output)
    return choice


def main():

    while True:
        choice = menu()
        if choice == '1':
            sync_fs_to_db()
        elif choice == '2':
            partial_sync()
        elif choice == '3':
            generate_playlist()
        elif choice == '4':
            export_altColumns()
        elif choice == '5':
            import_altColumns()
        else:
            break
        input("Press enter to go back to the main menu")
    print("Received config")


if __name__ == '__main__':
    main()
