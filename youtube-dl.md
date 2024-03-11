```shell
# For Instagram reels use yt-dlp
pip install yt-dlp
yt-dlp --cookies-from-browser chrome https://www.instagram.com/reel/Cim6BkkstwB/
```

```shell
# 137 mp4   1920x1080  1080p 4400k
# 299 mp4   1920x1080  1080p60 7377k
# 140 m4a   audio only DASH audio  129k

youtube-dl -ci -f 137+140/299+140/best -o "%(playlist_index)s-%(title)s.%(ext)s" 'url'
youtube-dl -ci -o "%(autonumber)s-%(title)s.%(ext)s" url
youtube-dl --playlist-start 133 -ci -f 137+140 'url'

# Other resolutions
# View available formats
youtube-dl -F <url>
# Download example (libav-tools package is needed)
youtube-dl -f 137+140 <url>

# Extract MP3 (ffmpeg package is needed)
youtube-dl --extract-audio --audio-format mp3 '<video URL>'
```
