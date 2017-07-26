* http://hackaday.com/2017/07/21/linux-fu-better-bash-scripting/

Try adding the following to `~/.inputrc` file:
```
# Use [Tab] and [Shift]+[Tab] to cycle through all the possible completions:
"\t": menu-complete
"\e[Z": menu-complete-backward
set completion-ignore-case
```
(breaks Home/End buttons and does not enter into directores)


```bash
#!/bin/bash

search_dir="/path/to/a/dir"

for subdir in "$search_dir"/*
do
  if [ ! -h "$subdir" ]
  then
    echo "$subdir"
    #ls "$subdir/data/0000/"
    rm -R "$subdir/data/0000/"
  fi
done
```
