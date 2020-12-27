Convert
* Linux: Sound Converter
    * http://soundconverter.org/
    * https://github.com/kassoulet/soundconverter
    * `apt install soundconverter`
* Linux: tags - EasyTag: `apt install easytag`
* (:question: - 2check) Linux: rip an audio CD: Sound Juicer
    * `apt install sound-juicer`
    * https://www.howtogeek.com/howto/20126/rip-audio-cds-with-sound-juicer/
    
Split
```shell
sudo apt install mp3splt

# Split at every 30 min
# this will produce files named "file_0000m_00s__0030m_00s.mp3", "file_0030m_00s__0060m_00s.mp3" etc.
mp3splt -t 30.0 file.mp3
```

Reduce bitrate
```shell
sudo apt install ffmpeg

ffmpeg -i file.mp3 -ab 64k -threads 4 file_64.mp3
# libmp3lame doesn't support multi-threading, so -threads n option is ignored
ffmpeg -h encoder=libmp3lame
...
Threading capabilities: none
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
    
#### Apply fadeout
* Make a selection
* Use `Effect` > `Fade Out` or `Effect` > `Studio Fade Out` tool (the last one might be under `Plug-in x to y` submenu)

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
