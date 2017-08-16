TODO:
* http://askubuntu.com/questions/115333/how-do-i-disable-the-sleep-button-on-my-keyboard/115423#115423
* http://www.noobslab.com/p/themes-icons.html
* http://www.webupd8.org/2016/03/mailnag-email-notifier-12-released-with.html
* http://mark.orbum.net/2012/05/14/disabling-dnsmasq-as-your-local-dns-server-in-ubuntu/

- [ ] grub settings
- [ ] NVIDIA driver (Software & Updates -> Additional Drivers)
- [ ] Keyboard settings (switch with Ctrl+Shift, use different layout for each window)
- [ ] `apt install gparted mc htop`
- [ ] Screensaver and lock settings
- [ ] Lates Remmina client
```bash
sudo add-apt-repository ppa:remmina-ppa-team/remmina-next
```
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
- [ ] Tweak Tool and Unity Tweak Tool
- [ ] Windows TTF fonts ([Download link](files/windows-ttf.zip))
```bash
# Copy to /usr/share/fonts/truetype or ~/.fonts/truetype/
# fc-cache is in package fontconfig
mkdir -p ~/.fonts/truetype/
unzip ~/Downloads/windows-ttf.zip -d ~/.fonts/truetype/
fc-cache -fv
```
- [ ] Infinality
```
add-apt-repository ppa:no1wantdthisname/ppa
apt update
apt install  fontconfig-infinality libfreetype6
# Config (current session)
/etc/fonts/infinality/infctl.sh setstyle
# Permanent settings: set USE_STYLE (USE_STYLE="DEFAULT" is fine)
# /etc/profile.d/infinality-settings.sh

# Uninstall
apt-get purge fontconfig-infinality
apt-get install ppa-purge
ppa-purge ppa:no1wantdthisname/ppa
```
- [ ] Disable dnsmasq (and remove libnss-mdns)
```shell
nano /etc/NetworkManager/NetworkManager.conf
# Comment out "dns=dnsmasq"
service network-manager restart
# If still there is no ping to .local domain names (but nslookup works)
apt remove libnss-mdns
```
- [ ] Gnome terminal
  * Edit -> Preferences -> General -> Open new terminals in: Tab
  * Switch tabs with Ctrl+Tab
 ```bash
 sudo apt install dconf-tools
 dconf-editor &
 # Org -> Gnome -> Terminal -> Legacy -> Keybindings
 # next-tab <Primary>Tab
 # prev-tab <Primary><Shift>Tab
 # If there is no 'Keybindings' item in the tree:
 gsettings set org.gnome.Terminal.Legacy.Keybindings:/org/gnome/terminal/legacy/keybindings/ next-tab '<Primary>Tab'
 gsettings set org.gnome.Terminal.Legacy.Keybindings:/org/gnome/terminal/legacy/keybindings/ prev-tab '<Primary><Shift>Tab'
 ```
   * Position
  ``` bash
  cp /usr/share/applications/gnome-terminal.desktop{,.bak}
  # Update 'Exec' parameters in  '[Desktop Entry]' and '[Desktop Action New]' sections:
  # Exec=gnome-terminal --geometry 127x43+490+290
  ```
- [ ] AES Crypt
  * https://www.aescrypt.com/download/
  * PCManFM integration: https://wiki.ubuntuusers.de/AES_Crypt/
