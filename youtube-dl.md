```shell
youtube-dl -ci -f 137+140/299+140/best -o "%(playlist_index)s-%(title)s.%(ext)s" 'url'
youtube-dl -ci -o "%(autonumber)s-%(title)s.%(ext)s" url
youtube-dl --playlist-start 133 -ci -f 137+140 'url'

# Other resolutions
# View available formats
youtube-dl -F <url>
# Download example (libav-tools package is needed)
youtube-dl -f 137+140 <url>
```
