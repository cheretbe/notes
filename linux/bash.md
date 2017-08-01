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

### If statement
The square brackets are a synonym for the test command. An if statement checks the exit status of a command in order to decide which branch to take. `grep -q "$text"` is a command, but `"$name" = 'Bob'` is not - it's just an expression. (https://stackoverflow.com/questions/8934012/when-square-brackets-are-required-in-bash-if-statement/8934070#8934070)

```bash
command1
if [ $? -ne 0 ]; then
    echo "command1 has failed"
fi

# Each command must be properly terminated, either by a newline or a semi-colon
if [ $? -ne 0 ] ; then echo 1; else echo 0 ; fi
```
