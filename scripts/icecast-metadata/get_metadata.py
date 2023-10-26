#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import datetime
import argparse
import random
import time
import contextlib
from streamscrobbler import streamscrobbler

@contextlib.contextmanager
def redirect_stdout():
    original = sys.stdout
    try:
        sys.stdout = open(os.devnull, 'w')
        yield
    finally:
        sys.stdout.close()
        sys.stdout = original

def get_current_track():
    # return(random.choice(["track1", "track2", "track3", "track4"]))
    try:
        with redirect_stdout():
            return streamscrobbler().getServerInfo("http://streaming.live365.com/b05055_128mp3").get("metadata")["song"].strip()
    except:
        return "api_error"

def add_item(item, file_name):
    item += "\n"
    with open(file_name, "a+") as f:
        f.seek(0)
        lines = f.readlines()
        if item not in lines:
            print(" writing " + item.rstrip("\n"))
            lines.append(item)
            lines.sort(key=lambda s: s.lower())
            f.seek(0)
            f.truncate()
            f.writelines(lines)

def main(args):
    previous_track = ""
    while True:
        track = get_current_track()
        print(datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S ") + track)
        if (track != previous_track) and (track != "api_error"):
            print(" trying to write " + track)
            add_item(track, args.out_file)
        previous_track = track
        time.sleep(60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("out_file", help="Output file")
    args = parser.parse_args()
    main(args)
