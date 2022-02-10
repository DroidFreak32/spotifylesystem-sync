import os
import sys
import taglib
from glob import glob

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def func(flac_files):
    for file in flac_files:
        print(os.path.relpath)


def find_flacs(music_dir):
    flac_files = []
    print("Scanning directory tree for flac files...")
    # for root, dirs, files in os.walk(music_dir, topdown=False):
    #     for file in files:
    #         if file.endswith(".flac"):
    #             flac_files.append(os.path.relpath(os.path.join(root, file), music_dir))
    flac_files = glob("**/*.flac", root_dir=music_dir, recursive=True)

    print("Size of list: " + str(flac_files.__sizeof__()))
    print(flac_files)
    return flac_files


def show_keys(music_root_dir, flac_files):
    print(music_root_dir, flac_files)
    for flac_file in flac_files:
        audiofile = taglib.File(os.path.join(music_root_dir, flac_file))
        print(audiofile.tags.keys(), audiofile.path)


if __name__ == '__main__':
    print_hi('PyCharm')
    music_root_dir = "/Users/rushab.shah/Music/Machine Gun Kelly"
    flac_files = find_flacs(music_root_dir)
    show_keys(music_root_dir, flac_files)
