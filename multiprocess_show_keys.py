import os
import subprocess
import sys
import taglib
from glob import glob
import asyncio
import multiprocessing
from itertools import repeat

global music_root_dir
music_root_dir = "/Users/rushab.shah/Music/Machine Gun Kelly"

def func(flac_files):
    for file in flac_files:
        print(os.path.relpath)


def find_flacs(music_dir):
    print("Scanning directory tree for flac files...")
    # for root, dirs, files in os.walk(music_dir, topdown=False):
    #     for file in files:
    #         if file.endswith(".flac"):
    #             flac_files.append(os.path.relpath(os.path.join(root, file), music_dir))
    flac_files = glob("**/*.flac", root_dir=music_dir, recursive=True)

    print("Size of list: " + str(flac_files.__sizeof__()))
    print(flac_files)
    return flac_files


# async def async_scan_keys(music_root_dir, flac_file):
#     audiofile = taglib.File(os.path.join(music_root_dir, flac_file))
#     print("ASYNC")
#     print(audiofile.tags.keys(), audiofile.path)
#
#
# async def async_scan_keys_sem(music_root_dir, flac_file):
#     async with sem:  # semaphore limits num of simultaneous downloads
#         return await async_scan_keys(music_root_dir, flac_file)
#
#
# async def main():
#     tasks = [
#         asyncio.ensure_future(async_scan_keys_sem(music_root_dir, flac_file))  # creating task starts coroutine
#         for flac_file in flac_files
#     ]
#     await asyncio.gather(*tasks)


def show_keys(flac_file, music_root_dir):
    print(music_root_dir, flac_file)
    audiofile = taglib.File(os.path.join(music_root_dir, flac_file))
    md5sum = subprocess.run(["metaflac", "--show-md5sum", audiofile.path], capture_output=True, universal_newlines=True).stdout.strip()

    audiofile_dict = dict()
    for key in list(audiofile.tags.keys()):
        # print(audiofile.tags[key])
        audiofile_dict[key] = audiofile.tags[key]
    audiofile_dict['MD5SUM'] = md5sum
    audiofile_dict['PATH'] = flac_file
    # loop = asyncio.get_event_loop()
    # try:
    #     loop.run_until_complete(main())
    # finally:
    #     loop.run_until_complete(loop.shutdown_asyncgens())
    #     loop.close()

    # for flac_file in flac_files:
    #     audiofile = taglib.File(os.path.join(music_root_dir, flac_file))
    #     md5sum = subprocess.run(["metaflac", "--show-md5sum", audiofile.path], capture_output=True)
    #     print(audiofile.tags.keys(), md5sum.stdout)

    return audiofile_dict


if __name__ == '__main__':
    multiprocessing.freeze_support()

    music_root_dir = "/Users/rushab.shah/Music/Machine Gun Kelly"

    flac_files = find_flacs(music_root_dir)
    pool = multiprocessing.Pool(8)
    result = pool.starmap(show_keys, zip(flac_files, repeat(music_root_dir)))
    pool.close()
    pool.join()
    print(result)
