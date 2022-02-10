import os
import subprocess
import sys
import taglib
from glob import glob
import asyncio
import multiprocessing
from itertools import repeat
import sqlite3

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
    # print(metadata)
    dbPath = os.path.join(music_root_dir, "testMusicDB.db")
    print("Checking path..")
    if os.path.exists(dbPath):
        conn = sqlite3.connect(dbPath)
        print("Opened database successfully")
        conn.execute('''create table IF NOT EXISTS MUSIC(
            TITLE TEXT NOT NULL,
            STREAMHASH CHAR(32) PRIMARY KEY NOT NULL,
            FILEPATH TEXT NOT NULL,
            ALBUM TEXT,
            LYRICS TEXT);''')
        conn.execute("""SELECT * FROM MUSIC""")
        for md in metadata:
            if not "LYRICS" in md:
                md["LYRICS"] = 'NULL'
                # print("Artist is albumartist")
            # print("PATH = " + md["PATH"] + " MD5SUM = " + md['MD5SUM'])
            conn.execute("INSERT INTO MUSIC(TITLE,ALBUM,LYRICS,STREAMHASH,FILEPATH) VALUES (?,?,?,?,"
                         "?) ON CONFLICT(STREAMHASH) DO UPDATE SET TITLE=TITLE,ALBUM=ALBUM,LYRICS=LYRICS,"
                         "FILEPATH=FILEPATH", (str(md["TITLE"]), md["ALBUM"], md['LYRICS'], md['MD5SUM'], md["PATH"]))
            # print(conn.total_changes)

        conn.commit()
        conn.close()


if __name__ == '__main__':
    main()


