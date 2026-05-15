#!/bin/bash

WATCH_DIR="/home/ubuntu/down"
SCRIPT="/home/ubuntu/file-organizer/organizer.py"

echo "[STARTED] Watching $WATCH_DIR"

while read FILE
do
    FULL_PATH="$WATCH_DIR/$FILE"
    echo "[EVENT] $FULL_PATH"

    /usr/bin/python3 "$SCRIPT" "$FULL_PATH" &
done < <(inotifywait -m -e close_write -e moved_to --format "%f" "$WATCH_DIR")