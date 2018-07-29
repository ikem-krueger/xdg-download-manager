#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import subprocess
import re

from inotify_simple import INotify, flags
from threading import Thread

def load_media_types(filename="media.types"):
    media_types_file = open(filename).read()

    media_types = {}
    
    reg_ex = r"(\w+\/.*\w)\s+\[(.*)\]"

    for mime_types, media_type in re.findall(reg_ex, media_types_file):
        for mime_type in re.split("\s", mime_types):
            media_types[mime_type] = media_type
            
    return media_types

def load_dest_dirs(filename="dest_dirs.json"):
    dest_dirs_file = open(filename)

    dest_dirs = json.load(dest_dirs_file)

    return dest_dirs

def get_mime_type(filename):
    mime_type = subprocess.check_output(["file", "--brief", "--mime-type", filename]).decode("utf-8").strip()

    print("mime_type: {}".format(mime_type))

    return mime_type

def get_media_type(filename):
    mime_type = get_mime_type(filename)
    media_type = media_types.get(mime_type, "UNKNOWN")

    print("media_type: {}".format(media_type))

    return media_type

def get_xdg_user_dir(name):
    xdg_user_dir = subprocess.check_output(["xdg-user-dir", name]).decode("utf-8").strip()
    
    return xdg_user_dir

def get_dest_dir(filename, verbose=True)
    media_type = get_media_type(filename)
    dest_dir = dest_dirs[media_type]

    if not os.path.isdir(dest_dir):
        name = dest_dir
        dest_dir = get_xdg_dir(name)

    if verbose:
        print("dest_dir: {}".format(dest_dir))

    return dest_dir

def move_file(filename, dry_run=False, notification=True):
    dest_dir = get_dest_dir(filename)
    
    if filename in blacklist: 
        print("Skip {}...".format(filename))
    else:
        print("Move {} to {}...".format(filename, dest_dir))

        if not dry_run and dest_dir != watch_dir:
            subprocess.call(["mv", "-f", filename, dest_dir])

        if notification:
            subprocess.call(["notify-send", "-i", "media-floppy", "Download finished!", filename])

def action(action, filename, *args):
    print("action: {}".format(action.__name__))

    action(filename, *args)

media_types = load_media_types()
dest_dirs = load_dest_dirs()

watch_dir = get_xdg_user_dir("DOWNLOAD")

blacklist = [".part"]

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
