- [ ] advanced settings on packages configuration (`dpkg-reconfigure debconf`, select "low priority") 
- [ ] grub settings (GRUB_RECORDFAIL_TIMEOUT=30, GRUB_TERMINAL=console)
- [ ] NTP time sync
```bash
systemctl status systemd-timesyncd --no-pager -l
# settings are in /etc/systemd/timesyncd.conf
# host names or IPs are separated by spaces
# NTP=0.ru.pool.ntp.org 1.ru.pool.ntp.org 2.ru.pool.ntp.org 3.ru.pool.ntp.org
# FallbackNTP=ntp.ubuntu.com
```
- [ ] Console font `sudo dpkg-reconfigure console-setup`
- [ ] Add root mail recipient in `/etc/aliases`
```bash
# to check
echo test | mail -s "test mail" root
```
