- [ ] Timezone
```bash
# CentOS 7
timedatectl list-timezones | grep Kaliningrad
timedatectl set-timezone Europe/Kaliningrad
# View current settings
timedatectl status
date
ls -l /etc/localtime
```

- [ ] NTP time sync
```bash
systemctl status chronyd --no-pager -l
chronyc sources
# settings are in /etc/chrony.conf
```

yum-cron?
