```shell
# For Instagram reels use yt-dlp
pip install yt-dlp
# https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-pass-cookies-to-yt-dlp
yt-dlp --cookies-from-browser chrome https://www.instagram.com/reel/Cim6BkkstwB/
# Use cookies from another host
# 1. Generate cookies.txt (just ignore "You must provide at least one URL" error)
yt-dlp -v --cookies-from-browser firefox --cookies cookies.txt
# 2. Copy cookies.txt
scp cookies.txt host.domain.tld:temp/
# 3. Use it on the remote host
yt-dlp -v --cookies cookies.txt https://www.youtube.com/watch?v=00000000000 --list-formats

# Youtube
# https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#format-selection-examples
yt-dlp -v --cookies cookies.txt https://www.youtube.com/watch?v=00000000000 --list-formats
# bv*: Select the best quality format that contains video. It may also contain audio.
# b: Select the best quality format that contains both video and audio
# -s, --simulate Do not download the video and do not write anything to disk
yt-dlp -v --cookies cookies.txt https://www.youtube.com/watch?v=00000000000 -f "bv*[ext=mp4][height<=1080]+ba[ext=m4a]/b[height<=1080]" -s
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
