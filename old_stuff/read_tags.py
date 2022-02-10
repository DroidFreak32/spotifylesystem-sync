import os
import sys
import taglib

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def func(music_dir):
    music_dir = "/Users/rushab.shah/Music/Machine Gun Kelly"
    print(os.walk(music_dir))
    flac_files = []
    print("Scanning directory tree for flac files...")
    for root, dirs, files in os.walk(music_dir, topdown=False):
        for file in files:
            if file.endswith(".flac"):
                flac_files.append(os.path.join(root, file))
    print(flac_files.__sizeof__())
    for flac_file in flac_files:
        audio = taglib.File(flac_file)
        print(os.path.basename(flac_file))
        print (str(audio.tags["TITLE"]))
        print(audio.channels)
if __name__ == '__main__':
    print_hi('PyCharm')
    func("a")