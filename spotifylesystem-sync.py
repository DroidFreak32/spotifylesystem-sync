from db_ops import complete_sync, partial_sync, generate_playlist

from common import cls
print("outside common")


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
            complete_sync()
        elif choice == '2':
            partial_sync()
        elif choice == '3':
            generate_playlist()
        elif choice == '4':
            generate_playlist()
        else:
            break
    print("Received config")


if __name__ == '__main__':
    main()
