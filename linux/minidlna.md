```shell
# View current value
cat /proc/sys/fs/inotify/max_user_watches
echo 1048576 > /proc/sys/fs/inotify/max_user_watches
```

Edit `/etc/sysctl.conf` to make this setting permanent:
```
fs.inotify.max_user_watches=1048576
```
