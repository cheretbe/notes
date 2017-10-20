

Ubuntu 16.04, if there are no records from previous boots (for example `journalctl -b1`). Edit `/etc/systemd/journald.conf`
and set `Storage=persistent`, then restart the service
```bash
systemctl restart systemd-journald
```
