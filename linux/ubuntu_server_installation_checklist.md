- [ ] advanced settings on packages configuration (`dpkg-reconfigure debconf`, select "low priority") 
- [ ] grub settings
```
GRUB_RECORDFAIL_TIMEOUT=30
GRUB_TERMINAL=console
```
- [ ] NTP time sync
```bash
systemctl status systemd-timesyncd --no-pager -l
# settings are in /etc/systemd/timesyncd.conf
# host names or IPs are separated by spaces
# NTP=0.ru.pool.ntp.org 1.ru.pool.ntp.org 2.ru.pool.ntp.org 3.ru.pool.ntp.org
# FallbackNTP=ntp.ubuntu.com
```
- [ ] Console font `sudo dpkg-reconfigure console-setup`
- [ ] Install `postfix` and add root mail recipient in `/etc/aliases` (to send copies to a local user: `root:	user@domain.tld,local-user`)
```bash
# check mail delivery ('mailutils' package needs to be installed)
echo test | mail -s "test mail" root
```
- [ ] Check journald [settings](./journalctl.md)
- [ ] Unattended updates (+ nagios notification)
```shell
apt install unattended-upgrades
nano /etc/apt/apt.conf.d/50unattended-upgrades
dpkg-reconfigure --priority=low unattended-upgrades
unattended-upgrade --debug --dry-run
```
![exclamation](https://github.com/cheretbe/notes/blob/master/images/warning_16.png) Add other repositories
* TODO: make a separate file with instructions, use:
     * http://www.richud.com/wiki/Ubuntu_Enable_Automatic_Updates_Unattended_Upgrades
     * https://askubuntu.com/questions/87849/how-to-enable-silent-automatic-updates-for-any-repository
     * :exclamation: see comments https://linux-audit.com/upgrading-external-packages-with-unattended-upgrade/
- [ ] Update umask value in `/etc/login.defs` (`UMASK 002`) if default ACLs are going to be used
- [ ] Remove mlocate (?)
```shell
# This removes /var/lib/mlocate/mlocate.db and a cron job to update this file
sudo apt purge mlocate
```

##### Physical machine
- [ ] Install smartmontools and [set parameters](https://github.com/cheretbe/notes/blob/master/linux/smart.md#smartd-settings)
- [ ] Check if smartd sends emails
