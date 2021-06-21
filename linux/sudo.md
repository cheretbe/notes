Rule matching debug


Create `/etc/sudo.conf` with the following content:
```
Debug sudo /var/log/sudo_debug.log all@debug
Debug sudoers.so /var/log/sudo_debug.log all@debug
```
:warning: Don't forget to remove it after debug, it's very verbose
