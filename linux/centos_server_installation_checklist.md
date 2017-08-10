- [ ] Timezone
```bash
timedatectl list-timezones | grep Kaliningrad
timedatectl set-timezone Europe/Kaliningrad
```

- [ ] NTP time sync
```bash
systemctl status chronyd --no-pager -l
chronyc sources
# settings are in /etc/chrony.conf
```
