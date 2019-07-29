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

Edit tracks: audacity<br>
https://www.audacityteam.org/
```shell
add-apt-repository ppa:ubuntuhandbook1/audacity
apt update
# Make sure it is the latest version
apt install audacity -s
```
