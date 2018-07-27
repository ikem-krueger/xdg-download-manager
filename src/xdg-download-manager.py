#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# - notifications for downloaded files that doesn't match mediatype
# - make use of mime icons
# - clamav!
# - syslog?

import subprocess

def get_xdg_folder(xdg_dest_dir):
    return subprocess.check_output(["xdg-user-dir", xdg_dest_dir])

def get_mime_type(file):
    return subprocess.check_output(["file", "--brief", "--mime-type", file])

def get_media_type(file):
    return subprocess.check_output("grep {0} /etc/media.types|cut -d[ -f2|cut -d] -f1".format(get_mime_type(file)), shell=True)

def move_file(file):
    xdg_dest_dir = get_xdg_folder(media_type[get_media_type(file)])

    if file.endswith(".part"): # Firefox workaround
        print("Skip {0}...".format(file))
    else:
        print("Move {0} to {1}...".format(file, xdg_dest_dir))

        subprocess.call(["mv", "-f", file, xdg_dest_dir])

        subprocess.call(["notify-send", "-i", "media-floppy", "Download finished!", file])

media_type = {
    "TEXT": "DOCUMENTS", 
    "OFFICE": "DOCUMENTS", 
    "BITMAP": "PICTURES", 
    "AUDIO": "MUSIC", 
    "VIDEO": "VIDEOS" 
}

/*
https://dustinoprea.com/2015/04/24/using-inotify-to-watch-for-directory-changes-from-python/

inotifywait xdg_download_dir --monitor --quiet --event close_write,moved_to --format "%f"|\
while read file
do
  https://www.saltycrane.com/blog/2008/09/simplistic-python-thread-example/
  
  move_file(file) &
done
*/
