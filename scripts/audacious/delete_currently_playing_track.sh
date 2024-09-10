#!/bin/bash
# Deletes the currently playing song from the filesystem and from the playlist.
# https://redmine.audacious-media-player.org/boards/1/topics/1870
set -eu
set -o pipefail

# Avoid accidentally deleting next song if pressed delete too late and it
# already advanced to the next song.
seconds_playing="$(audtool current-song-output-length-seconds)" 
if [ $seconds_playing -gt 5 ]; then
    fpath="$(audtool current-song-filename)" 
    # mv "$fpath" ~/.local/share/Trash/files
    rm "$fpath"
    playlist_pos="$(audtool playlist-position)" 
    audtool playlist-delete "$playlist_pos"
    sleep 0.5
    audtool playlist-jump "$playlist_pos"
    audtool playback-play
    notify-send -t 3000 "DELETED: $fpath" 
fi