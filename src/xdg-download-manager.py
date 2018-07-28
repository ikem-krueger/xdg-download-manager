#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

def load_media_types(filename="media.types"):
    media_types_file = open(filename).read()

    media_types = {}
    
    reg_ex = r"(\w+\/.*\w)\s+\[(.*)\]"

    for mime_types, media_type in re.findall(reg_ex, media_types_file):
        for mime_type in re.split("\s", mime_types):
            media_types[mime_type] = media_type
            
    return media_types

def load_xdg_folder(filename="xdg_folder.json"):
    return json.load(open(filename))

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

    if filename in blacklist: 
        print("Skip {}...".format(filename))
    else:
        print("Move {} to {}...".format(filename, xdg_dest_dir))

        if not dry_run:
            subprocess.call(["mv", "-f", filename, xdg_dest_dir])

        subprocess.call(["notify-send", "-i", "media-floppy", "Download finished!", filename])

def action(action, filename, *args):
    print("action: {}".format(action.__name__))

    action(filename, *args)

watch_dir = get_xdg_folder("DOWNLOAD", verbose=False)

blacklist = [".part"]

media_types = load_media_types()
xdg_folder = load_xdg_folder()

# https://pypi.org/project/inotify_simple/
inotify = INotify()

watch_flags = flags.CLOSE_WRITE | flags.MOVED_TO

inotify.add_watch(watch_dir, watch_flags)

for event in inotify.read():
    filename = watch_dir + "/" + event.name
    
    print("watch_dir: {}".format(watch_dir))
    print("filename: {}".format(filename))

    # https://www.saltycrane.com/blog/2008/09/simplistic-python-thread-example/
    t = Thread(target=action, args=(move_file, filename))
    t.start()

