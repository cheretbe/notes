

Ubuntu 16.04, if there are no records from previous boots (for example `journalctl -b1`). Edit `/etc/systemd/journald.conf`
and set `Storage=persistent`, then restart the service
```bash
systemctl restart systemd-journald
```
Set `SystemMaxUse` parameter (e.g. `SystemMaxUse=500M`) because by default it is set to 10% of the size of the respective file system.

* https://askubuntu.com/questions/765315/how-to-find-previous-boot-log-after-ubuntu-16-04-restarts
* https://wiki.archlinux.org/index.php/Systemd#Journal

```shell
# See the boots that journald knows about
journalctl --list-boots
# See logs from particular units
journalctl -u nginx.service
journalctl -u nginx.service -u php-fpm.service --since today
# Monitor new messages
journalctl --since now -f
# View logs from other system (mounted on /mountpoint) -D DIR, --directory=DIR
journalctl --directory=/mountpoint/var/log/journal/<machine-id>
```
