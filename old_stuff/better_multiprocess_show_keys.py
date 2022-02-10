import os
import subprocess
import sys
import taglib
from glob import glob
import asyncio
import multiprocessing
from itertools import repeat

def find_flacs(music_dir):
    print("Scanning directory tree for flac files...")
    # for root, dirs, files in os.walk(music_dir, topdown=False):
    #     for file in files:
    #         if file.endswith(".flac"):
    #             flac_files.append(os.path.relpath(os.path.join(root, file), music_dir))
    flac_files = glob("**/*.flac", root_dir=music_dir, recursive=True)

    print("Size of list: " + str(flac_files.__sizeof__()))
    # print(flac_files)
    return flac_files


def asyncmetadata(music_dir, flac_file):
    audiofile = taglib.File(os.path.join(music_dir, flac_file))
    md5sum = subprocess.run(["metaflac", "--show-md5sum", audiofile.path], capture_output=True, universal_newlines=True).stdout.strip()
    audiofile_dict = dict()
    for key in list(audiofile.tags.keys()):
        # print(audiofile.tags[key])
        audiofile_dict[key] = str(audiofile.tags[key])
    audiofile_dict['MD5SUM'] = md5sum
    audiofile_dict['PATH'] = flac_file
    print(audiofile_dict)
    return audiofile_dict

def generate_metadata(music_dir, flac_files):
    a_pool = multiprocessing.Pool(8)
    result = a_pool.starmap(asyncmetadata, zip(repeat(music_dir), flac_files))
    return result

def main():

    global music_root_dir

    music_root_dir = "/Users/rushab.shah/Music/Machine Gun Kelly"

    flac_files = find_flacs(music_root_dir)
    metadata = generate_metadata(music_root_dir, flac_files)
    print(metadata)


if __name__ == '__main__':
    main()


