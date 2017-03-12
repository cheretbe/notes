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
# check mail delivery
echo test | mail -s "test mail" root
```
- [ ] Unattended updates (+ nagios notification)
```shell
apt install unattended-upgrades
nano /etc/apt/apt.conf.d/50unattended-upgrades
dpkg-reconfigure --priority=low unattended-upgrades
unattended-upgrade --debug --dry-run
```
![exclamation](https://github.com/cheretbe/notes/blob/master/images/warning_16.png) Add other repositories
* TODO: make a separate file with instructions (use http://www.richud.com/wiki/Ubuntu_Enable_Automatic_Updates_Unattended_Upgrades)

##### Physical machine
- [ ] Install smartmontools and [set parameters](https://github.com/cheretbe/notes/blob/master/linux/smart.md#smartd-settings)
- [ ] Check if smartd sends emails
