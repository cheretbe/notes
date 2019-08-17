TODO:
* http://askubuntu.com/questions/115333/how-do-i-disable-the-sleep-button-on-my-keyboard/115423#115423
* http://www.noobslab.com/p/themes-icons.html
* http://www.webupd8.org/2016/03/mailnag-email-notifier-12-released-with.html
* http://mark.orbum.net/2012/05/14/disabling-dnsmasq-as-your-local-dns-server-in-ubuntu/
* 18.04
    * https://www.gnome-look.org/p/1207034/
    * Move the clock: http://frippery.org/extensions/ (Gnome version is in `/usr/share/gnome/gnome-version.xml`)
    * Ctrl+Shift setiing is in Gnome-tweaks, `Keyboard & Mouse` > `Additional Layout Options`

- [ ] grub settings
- [ ] NVIDIA driver (Software & Updates -> Additional Drivers)
- [ ] Keyboard settings (switch with Ctrl+Shift, use different layout for each window)
- [ ] `apt install gparted mc htop`
- [ ] Screensaver and lock settings
- [ ] PCManFM
- [ ] Latest Remmina client
```bash
sudo add-apt-repository ppa:remmina-ppa-team/remmina-next
```
- [ ] Change time from UTC to local (when dual-booting with Windows)
```bash
timedatectl set-local-rtc 1
# turn UTC back on
timedatectl set-local-rtc 1
# view current setting
timedatectl

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
- [ ] ~~[Ambiance Crunchy Theme](http://www.noobslab.com/2016/06/ambiance-crunchy-themes-suite-is-now.html)~~ http://www.noobslab.com/2016/03/ambiance-radiance-colors-theme-suite.html
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
- [ ] Ublock Origin
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
  * Colors
  ```
  Themes: 'White on black' + 'Tango'
  Terminal background color: #0E1C4A (R:14 G:28 B:74) or #0B1437 (R:11 G:20 B:55)
  ```
- [ ] AES Crypt
  * https://www.aescrypt.com/download/
  * PCManFM integration: https://wiki.ubuntuusers.de/AES_Crypt/
- [ ] Mouse wheel scroll speed
```bash
sudo apt-get install imwheel
nano ~/.imwheelrc
```
```
".*"
None,      Up,   Button4, 3
None,      Down, Button5, 3
Control_L, Up,   Control_L|Button4
Control_L, Down, Control_L|Button5
Shift_L,   Up,   Shift_L|Button4
Shift_L,   Down, Shift_L|Button5
```
The last 4 lines in the code above are there to allow Ctrl / Shift with mouse scroll wheel up / down to work (for instance, to allow zooming in on a webpage in the web browser, etc.), which is the default behaviour.
```shell
# --kill kills previous instance if exists
imwheel --kill
```
Open Startup Applications, click "Add" and under both "Name" and "Command" fields, add "imwheel --kill"
* http://www.webupd8.org/2015/12/how-to-change-mouse-scroll-wheel-speed.html
