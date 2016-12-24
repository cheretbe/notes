- [ ] grub settings
- [ ] Keyboard settings (switch with Ctrl+Shift, use different layout for each window)
- [ ] `apt install parted mc htop`
- [ ] Screensaver and lock settings
- [ ] Change time from UTC to local (when dual-booting with Windows)
```bash
timedatectl set-local-rtc 1
# view current settings
timedatectl
# turn UTC back on
timedatectl set-local-rtc 1
# pre-16.04: add UTC=no to /etc/default/rcS 
```
- [ ] NTP time sync
```bash
systemctl status systemd-timesyncd --no-pager -l
# settings are in /etc/systemd/timesyncd.conf
# host names or IPs are separated by spaces
# NTP=0.ru.pool.ntp.org 1.ru.pool.ntp.org 2.ru.pool.ntp.org 3.ru.pool.ntp.org
# FallbackNTP=ntp.ubuntu.com
```
- [ ] Install Windows TTF fonts ([Download link](files/windows-ttf.zip))
```bash
# Copy to /usr/share/fonts/truetype or ~/.fonts/truetype/
# fc-cache is in package fontconfig
unzip ~/Downloads/windows-ttf.zip -d ~/.fonts/truetype/
fc-cache -fv
```
