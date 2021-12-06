Default setting in `/etc/systemd/journald.conf` is `Storage=auto` which implies that systemd journaling will only persist the journal if the expected storage location is available. Otherwise, the journal data is stored in memory and lost between reboots.<br>
Create it to keep and query events from previous boots.
```shell
mkdir -p /var/log/journal
systemd-tmpfiles --create --prefix /var/log/journal
systemctl restart systemd-journald
```
Another option is to set `Storage=persistent` parameter
* `SystemMaxUse` is `10%` for peristent storage in `/var/log/journal`, or `15%` for memory use in `/run/log/journal`
    * It could be set to a specific size (e.g. `SystemMaxUse=500M`) if default 10% of the size of the respective file system is too much
* `SystemMaxFiles=100`
* `SystemMaxFileSize = SystemMaxUse/8`


```bash
journalctl --disk-usage

# The service outputs storage limits on start 
systemctl status systemd-journald
# It might be possible to get storage settings programatically by parsing JSON output
# and extracting values like CURRENT_USE, MAX_USE, DISK_AVAILABLE etc.
journalctl -b 0 -u systemd-journald -o json-pretty
```
* https://askubuntu.com/questions/765315/how-to-find-previous-boot-log-after-ubuntu-16-04-restarts
* https://wiki.archlinux.org/index.php/Systemd#Journal

```shell
# Filter by priority
#   0: emerg
#   1: alert
#   2: crit
#   3: err
#   4: warning
#   5: notice
#   6: info
#   7: debug
# 0-4 from current boot
journalctl -b --no-pager -p warning 
# See the boots that journald knows about
journalctl --list-boots

# See logs from particular units
journalctl -u nginx.service
journalctl -u nginx.service -u php-fpm.service --since today

# Show entries with the specified syslog identifier 
# -t --identifier=STRING
# [!!!] Doesn't support partial matching and wildcards, use grep
journalctl -t dnf
journalctl | grep dnf

# View the list of field names for match arguments (_PID, _COMM, etc.)
man systemd.journal-fields
# See messages by PID
journalctl -b 0 _PID=9400
# See messages by process name
journalctl -b 0 _COMM=mailnag

# Time window
journalctl --since "2015-01-14" --until "2015-01-15 03:00"
journalctl --since "15 min ago"
journalctl --since yesterday
journalctl --since today

# Last n lines
# -n --lines[=INTEGER]
journalctl -n 10 --no-pager


# Monitor new messages
journalctl --since now -f
# View logs from other system (mounted on /mountpoint) -D DIR, --directory=DIR
# This only works with "Storage=persistent", by default current boot log is
# only temporarily stored in a place like /run/log/journal
journalctl --directory=/mountpoint/var/log/journal/<machine-id>

# Cleanup
journalctl --vacuum-size=100M
journalctl --vacuum-time=2d
# Purge as much as possible
journalctl --flush --rotate
journalctl --vacuum-time=1s

```

Write to the journal from a script
```shell
# -p, --priority: alert, crit, err, warning, notice, info, debug (defaults to "info")
echo "hello" | systemd-cat -t "my-script" -p info 

# Redirect output of a process to the journal
systemd-cat -t "certbot-cron" /usr/bin/certbot --renew
journalctl -t "certbot-cron"
```
* https://www.ctrl.blog/entry/how-to-cron-to-journal.html
