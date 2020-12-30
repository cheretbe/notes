

Ubuntu 16.04, if there are no records from previous boots (for example `journalctl -b1`). Edit `/etc/systemd/journald.conf`
and set `Storage=persistent`, then restart the service
```bash
systemctl restart systemd-journald

journalctl --disk-usage

# The service outputs storage limits on start 
systemctl status systemd-journald
```
Set `SystemMaxUse` parameter (e.g. `SystemMaxUse=500M`) because by default it is set to 10% of the size of the respective file system.

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
