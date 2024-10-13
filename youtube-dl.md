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
# 399+140/b is just an example: video 399(mp4 1920x1080 60) + audio 140(m4a 129k 44k) or the best combined format
yt-dlp -v --cookies cookies.txt -f "399+140/b" https://www.youtube.com/watch?v=00000000000
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
