#!/bin/sh

# - notifications for downloaded files that doesn't match mediatype
# - make use of mime icons
# - clamav!
# - syslog?

XDG_CONFIG_DIR="$HOME/.config"

# import XDG folder variables
. "$XDG_CONFIG_DIR/user-dirs.dirs"

move_to(){

XDG_DEST_DIR="$1"

echo "Move $FILE to $XDG_DEST_DIR.."

notify-send -i media-floppy "Download finished!" "$FILE"

mv -f "$FILE" "$XDG_DEST_DIR"
}

get_type(){

MIME_TYPE=$(file --brief --mime-type "$FILE")
MEDIA_TYPE=$(grep "$MIME_TYPE" /etc/media.types|cut -d[ -f2|cut -d] -f1)

if (echo "$FILE"|grep -q ".part$") # Firefox workaround
then
  echo "Skip $FILE.."
else
  case $MEDIA_TYPE in
    TEXT)   move_to "$XDG_DOCUMENTS_DIR";;
    OFFICE) move_to "$XDG_DOCUMENTS_DIR";;
    BITMAP) move_to "$XDG_PICTURES_DIR";;
    AUDIO)  move_to "$XDG_MUSIC_DIR";;
    VIDEO)  move_to "$XDG_VIDEOS_DIR";;
  esac
fi
}

cd "$XDG_DOWNLOAD_DIR"

inotifywait . --monitor --quiet --event close_write,moved_to --format "%f"|\
while read FILE
do
  get_type "$FILE" &
done

