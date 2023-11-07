```shell
# watch for lines:
# System clock synchronized: yes
#               NTP service: active
timedatectl status
```

### Chrony

* https://coelhorjc.wordpress.com/2015/01/19/how-to-syncronize-time-in-linux-using-ntp-openntpd-systemd-timesyncd-and-chrony/
* https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/7/html/System_Administrators_Guide/sect-Using_chrony.html

```shell
cat /etc/chrony/chrony.conf
chronyc ntpdata
```

### systemd

```shell
systemctl status systemd-timesyncd
# settings are in /etc/systemd/timesyncd.conf
# host names or IPs are separated by spaces
# NTP=0.ru.pool.ntp.org 1.ru.pool.ntp.org 2.ru.pool.ntp.org 3.ru.pool.ntp.org
# FallbackNTP=ntp.ubuntu.com
/etc/systemd/timesyncd.conf
systemctl restart systemd-timesyncd
```
