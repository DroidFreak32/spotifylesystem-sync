# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import sys
import taglib

import tinytag as TinyTag
from mutagen.flac import FLAC
import json

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def get_title_and_artist(music_dir):
    """Recursively reads local files in indicated music_dir and yields a string 'song - artist'"""
    if len(music_dir) == 0 or not os.path.isdir(music_dir):
        while True:
            music_dir = input("Please paste the path to your music directory:")

            if os.path.isdir(music_dir):
                break

            print(
                "The provided path is not valid. Please try again or type "
                "in the path directly into the source code if there's "
                "issues\n(use Ctrl + C to exit the program)"
            )
    else:
        print(f"Found valid path. Commencing search in {music_dir}")

    files_read = 0
    for root, dirs, files in os.walk(music_dir):
        files = [fi for fi in files if fi.endswith(".flac")]
        for file in files:
            print(os.path.join(root, file))
            # try:
                # audiofile = TinyTag.get(os.path.join(root, file))
                # audio = FLAC(os.path.join(root, file))
            # except:
            #     continue
            audio = taglib.File(os.path.join(root, file))
            files_read += 1
            jsonobj = audio
            # print(jsonobj.pprint())
            try:
                print(audio.tags["ALBUM"])
            except:
                continue
            # yield (f"track:{audiofile.title} artist:{audiofile.artist}", f"{audiofile.artist} - {audiofile.title}")
            # NOTE: Query being in double quotes makes it stick to the
            # given word order instead of matching a bunch of possibilities
            # Use it (by writing \" at the beginning and end of the string)
            # if you are not happy with the matches found

    if files_read == 0:
        print(
            "\nNo files found at the specified location."
            "Please check the path to the directory is correct."
        )
        sys.exit()

    print(
        f"\nRead {files_read} files. Make sure to check for any possible "
        'unread files due to "Lame tag CRC check failed" or similar.\n'
        "Those come from an external library and this software cannot "
        "account for them"
    )

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    # audio = FLAC(r"G:\Shared drives\Muzik\Bring Me the Horizon\2013 - Sempiternal\Bring Me the Horizon - Hospital for Souls.flac")
    # jsonobj = audio
    # print(jsonobj.pprint())
    # print(audio.keys())
    # music_dir = "G:\\Shared drives\\Muzik\\Bring Me the Horizon"
    music_dir = "/Users/rushab.shah/Music/Machine Gun Kelly"
    # Write the dirpath directly here to avoid having to do it through terminal.
    # Make sure to escape backslashes. Examples:
    # 'C:/Users/John/Music/My Music'
    # "C:\\Users\\John\\Music\\My Music"
    print(FLAC().keys())
    print("\n\n\n\n\n")
    get_title_and_artist(music_dir)
    # print(f"searched_songs: {query_song_pair[1]}")
    print("Searched!")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
