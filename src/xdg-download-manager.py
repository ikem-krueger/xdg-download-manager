#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# - clamav!
# - blacklist
# - dry run mode
# - manual sort mode
# - recursive sort

import json
import subprocess
import re

from inotify_simple import INotify, flags
from threading import Thread

def get_xdg_folder(name, verbose=True):
    xdg_folder = subprocess.check_output(["xdg-user-dir", name]).decode("utf-8").strip()
    
    if verbose:
        print("xdg_dest_dir: {}".format(xdg_folder))
    
    return xdg_folder

def load_media_types():
    media_types_file = open("media.types").read()

    media_types = {}
    
    reg_ex = r"(\w+\/.*\w)\s+\[(.*)\]"

    for mime_types, media_type in re.findall(reg_ex, media_types_file):
        for mime_type in re.split("\s", mime_types):
            media_types[mime_type] = media_type
            
    return media_types

def get_mime_type(filename):
    mime_type = subprocess.check_output(["file", "--brief", "--mime-type", filename]).decode("utf-8").strip()

    print("mime_type: {}".format(mime_type))

    return mime_type

def get_media_type(filename):
    mime_type = get_mime_type(filename)
    media_type = media_types.get(mime_type, "OTHER")

    print("media_type: {}".format(media_type))

    return media_type

def move_file(filename, dry_run=False):
    media_type = get_media_type(filename)
    xdg_dest_dir = get_xdg_folder(xdg_folder[media_type])

    if filename.endswith(".part"): # Firefox workaround
        print("Skip {}...".format(filename))
    else:
        print("Move {} to {}...".format(filename, xdg_dest_dir))

        if not dry_run:
            subprocess.call(["mv", "-f", filename, xdg_dest_dir])

        subprocess.call(["notify-send", "-i", "media-floppy", "Download finished!", filename])

xdg_download_dir = get_xdg_folder("DOWNLOAD", verbose=False)

media_types = load_media_types()

xdg_folder = json.load(open("xdg_folder.json"))

# https://pypi.org/project/inotify_simple/
inotify = INotify()
watch_flags = flags.CLOSE_WRITE | flags.MOVED_TO
wd = inotify.add_watch(xdg_download_dir, watch_flags)

for event in inotify.read():
    filename = xdg_download_dir + "/" + event.name
    
    print("filename: {}".format(filename))

    # https://www.saltycrane.com/blog/2008/09/simplistic-python-thread-example/
    t = Thread(target=move_file, args=(filename, ))
    t.start()

