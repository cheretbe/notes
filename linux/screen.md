Save scrollback buffer (screen contents + history) to a file  
<kbd>Ctrl</kbd>+<kbd>A</kbd> `:hardcopy -h /tmp/screen.txt`
Increase scrollback buffer
<kbd>Ctrl</kbd>+<kbd>A</kbd> `:scrollback 10000`
Permanent setting - add to `~/.screenrc`:
```
scrollback 10000
```
