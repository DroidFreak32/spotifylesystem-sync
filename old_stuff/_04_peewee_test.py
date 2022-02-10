import os
import subprocess
import sys
import zlib
from base64 import b64encode
from base64 import b64decode

import taglib
from glob import glob
import asyncio
import pathos.multiprocessing as multiprocessing
from itertools import repeat
import sqlite3
from peewee import *

db = SqliteDatabase(":memory:")


class Music(Model):
    STREAMHASH = CharField(max_length=32, primary_key=True, unique=True)
    PATH = TextField(unindexed=True)

    class Meta:
        database = db



def main():

    # print(metadata)
    db.connect()
    db.drop_tables([Music])
    db.create_tables([Music])
    music_db_orm = None

    tmp_array = ["ABCD", "ABCE", "ABCF", "ABCD"]
    i = 1
    for ar in tmp_array:
        try:
            music_db_orm = Music.create(STREAMHASH=str(ar), PATH=str(ar))

        except IntegrityError as IE:
            music_db_orm.save()
            print("Exception Raised!")
            query = Music.select().dicts()
            for row in query:
                print("Printing all rows")
                print(row)
            print(str(IE))
            raise IE

    music_db_orm.save()


if __name__ == '__main__':
    main()
