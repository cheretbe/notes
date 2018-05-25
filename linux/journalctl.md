

Ubuntu 16.04, if there are no records from previous boots (for example `journalctl -b1`). Edit `/etc/systemd/journald.conf`
and set `Storage=persistent`, then restart the service
```bash
systemctl restart systemd-journald
```
* https://askubuntu.com/questions/765315/how-to-find-previous-boot-log-after-ubuntu-16-04-restarts
* https://wiki.archlinux.org/index.php/Systemd#Journal

```shell
journalctl --list-boots
```
