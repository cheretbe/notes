Convert
* Linux: Sound Converter
    * http://soundconverter.org/
    * https://github.com/kassoulet/soundconverter
    * `apt install soundconverter`
* Linux: tags - EasyTag: `apt install easytag`
* (:question: - 2check) Linux: rip an audio CD: Sound Juicer
    * `apt install sound-juicer`
    * https://www.howtogeek.com/howto/20126/rip-audio-cds-with-sound-juicer/

Adjust level
```shell
# mp3gain does not just do peak normalization,  as many normalizers do. Instead, it does some
# statistical analysis to  determine how loud the file actually sounds to the human ear. Also,
# the  changes mp3gain makes are completely lossless. There  is no quality lost in the change
# because the program adjusts the mp3 file  directly, without decoding and re-encoding. Also,
# this works with all mp3  players, i.e. no support for a special tag or something similar is  required.
sudo snap install mp3gain

# -r  apply Track gain automatically (all files set to equal loudness)
mp3gain -r *.mp3
# -c  ignore clipping warning when applying gain
mp3gain -c -r *.mp3

# -g i   apply gain i to mp3 without  doing any analysis
mp3gain -g -8 track.mp3
```
    
Split
```shell
# Capture ans split an http(s) stream
# -map 0 maps everything from input to output (https://ffmpeg.org/ffmpeg.html#toc-Stream-selection)
# 3600s = 1 hour
ffmpeg -i https://streaming.live365.com/b05055_128mp3 -f segment -segment_time 3600 -c copy -map 0 "output_%4d.mp3"

sudo apt install mp3splt

# Split at every 30 min
# this will produce files named "file_0000m_00s__0030m_00s.mp3", "file_0030m_00s__0060m_00s.mp3" etc.
mp3splt -t 30.0 file.mp3
```

ffmpeg installation
```shell
sudo apt install ffmpeg
# or
sudo snap install ffmpeg
# [!!!] Note that snap version will not have access to arbitrary file paths, only to some hard-coded locations
# https://askubuntu.com/a/1033617
# https://bugs.launchpad.net/ubuntu/+source/snapd/+bug/1643706
snap connections | grep ffmpeg
# By default it even doesn't have access to /media
sudo snap connect ffmpeg:removable-media
```

Reduce bitrate
```shell
ffmpeg -i file.mp3 -ab 64k -threads 4 file_64.mp3
# libmp3lame doesn't support multi-threading, so -threads n option is ignored
ffmpeg -h encoder=libmp3lame
...
Threading capabilities: none
```
Convert from m4b to mp3
```shell
# m4b is just a fancy name for an AAC file
# This creates a single MP3 file, just use mp3splt afterwards
# Non-working fancy solution below
ffmpeg -i source.m4b -acodec libmp3lame -ab 64k output.mp3

# This script almost works, but something is wrong with parameters
# Debug when there will be some free time (csv parsing works, use 'set -x' to see what's going on next)
# https://stackoverflow.com/questions/30305953/is-there-an-elegant-way-to-split-a-file-by-chapter-using-ffmpeg/53553938#53553938
```

Test integrity
```shell
# Note: the null muxer does not generate any output, but specifying an output
# file is required by the ffmpeg syntax. That's why "-f null -" is used
find . -iname '*.mp3' -exec echo {} \; -exec ffmpeg -v error -i {} -f null - \; ;finished
# TODO: find a way to extract errors together with file name
# starting point:
ffmpeg.exe -v error -i file.avi -f null - >error.log 2>&1
```

### Edit tracks: audacity
* https://www.audacityteam.org/
```shell
add-apt-repository ppa:ubuntuhandbook1/audacity
apt update
# Make sure it is the latest version
apt install audacity -s
```

#### Trim a file
* Move the cursor to the time that is currently being played
    * Press `Pause`
    * Press <kbd>X</kbd> key (`Transport` > `Play` > `Play/Stop and Set Cursor`)
* Extend selection using `Select` > `Region` > `Track Start to Cursor` (or `Cursor to Track End`)
* `Edit` > `Remove Special` > `Trim Audio`
* If trimming has not been applied from the start, move selection to the start of the track
    * Select `Time Shift Tool`
    * Click and drag to the start of the track
    
#### Apply a fade effect
* Make a selection
* Use `Effect` > `Fade Out` or `Effect` > `Studio Fade Out` tool (the last one might be under `Plug-in x to y` submenu)


### Console spectrum analyzer: cli-visualizer

https://github.com/dpayne/cli-visualizer
```shell
apt install cmake libncursesw5-dev libpulse-dev libfftw3-dev
```
* run `install.sh` as an ordinary user (it asks for sudo password), this way you get a default config in `~/.config/vis`
* `cp cli-visualizer/examples/old_rainbow ~/.config/vis/colors/`
* `nano ~/.config/vis/config`
* `audio.stereo.enabled=false`
* `colors.scheme=old_rainbow`

`~/.local/share/applications/cli-visualizer.desktop`
```
[Desktop Entry]
Type=Application
Comment=Command Line Visualizer
Terminal=false
Exec=gnome-terminal --class=CliVisualizer --title "Command Line Visualizer" --geometry=130x17 --hide-menubar --zoom=0.3 --profile cli-visualizer -- /usr/local/bin/vis
StartupWMClass=CliVisualizer
Name=Command Line Visualizer
Icon=/home/user/.local/share/icons/hicolor/48x48/apps/Apps-Volume-Equalizer-icon.png
X-Ubuntu-Gettext-Domain=cli-visualizer
```
* :warning: Don't forget to create `cli-visualizer` profile (disabling scrollbar, for example)
* [Apps-Volume-Equalizer-icon.png](./files/icons/Apps-Volume-Equalizer/Apps-Volume-Equalizer-icon.png)
* use `--geometry=130x17+3394+160` to set an exact window position (use `xwininfo` to find out current position and geometry)
* Add to desktop `ln -s ~/.local/share/applications/cli-visualizer.desktop ~/Desktop/cli-visualizer.desktop`
* TODO: toggle title bar on/off
   * https://unix.stackexchange.com/questions/420452/how-to-hide-title-bar-for-a-specific-window/422587#422587
       * Find out why it doesn't work before writing own script: https://askubuntu.com/questions/928226/xprop-fails-to-undecorate-window/931874#931874
   * starting point (Python 2): https://askubuntu.com/questions/928226/xprop-fails-to-undecorate-window
   * hints on Python 3 version: https://stackoverflow.com/questions/10415097/window-position-a-little-off-just-after-spawning-and-moving-using-python-wnck
