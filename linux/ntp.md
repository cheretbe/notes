```shell
# watch for lines:
# System clock synchronized: yes
#               NTP service: active
timedatectl status

# the only relatively easy way to check random NTP server availability
apt install python3-ntplib
python3 -c "import ntplib; exit(0 if ntplib.NTPClient().request('ntp.pt.corp', timeout=5) else 1)"
# Ansible version
ansible -m ansible.builtin.apt -a '{"name": ["python3-ntplib"]}' --become host.domain.tld
ansible -a "python3 -c \"import ntplib; exit(0 if ntplib.NTPClient().request('pool.ntp.org', timeout=5) else 1)\"" host.domain.tld
```

### Chrony

* https://coelhorjc.wordpress.com/2015/01/19/how-to-syncronize-time-in-linux-using-ntp-openntpd-systemd-timesyncd-and-chrony/
* https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/7/html/System_Administrators_Guide/sect-Using_chrony.html

```shell
cat /etc/chrony/chrony.conf
chronyc tracking
# ^*, ^+ are good, ^* is bad, use -v to get details
chronyc -n sources
chronyc ntpdata

# ntpdate -q alternative:
# may need to temporarily stop chrony service
chronyd -q 'server 192.168.0.100 iburst'
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
