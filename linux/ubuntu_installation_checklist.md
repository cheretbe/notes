TODO:
* http://askubuntu.com/questions/115333/how-do-i-disable-the-sleep-button-on-my-keyboard/115423#115423
* http://www.noobslab.com/p/themes-icons.html
* http://www.webupd8.org/2016/03/mailnag-email-notifier-12-released-with.html
* http://mark.orbum.net/2012/05/14/disabling-dnsmasq-as-your-local-dns-server-in-ubuntu/
* 18.04
    * DNS fix + `apt purge avahi-daemon`? (check if removing avahi-daemon is enough for 18.04.03)
    * Move windows to other monitor: <kbd>Win</kbd>+<kbd>Shift</kbd>+arrows
    * Themes
        * https://www.gnome-look.org/p/1207034/
        * https://github.com/valr/awf
        * https://github.com/themix-project/oomox
        * https://github.com/Jannomag/Yaru-Colors
    * Move the clock: http://frippery.org/extensions/ (Gnome version is in `/usr/share/gnome/gnome-version.xml`)
    * Ctrl+Shift setting is in Gnome-tweaks, `Keyboard & Mouse` > `Additional Layout Options`
    * https://itsfoss.com/ubuntu-shortcuts/
    * https://askubuntu.com/questions/1042641/how-to-set-custom-lock-screen-time-in-ubuntu-18-04
    * `2check`: https://askubuntu.com/questions/1048774/disabling-lock-screen-18-04/1064704#1064704
    * Click to minimize: `gsettings set org.gnome.shell.extensions.dash-to-dock click-action 'minimize-or-previews'`
        * view available actions: `gsettings range org.gnome.shell.extensions.dash-to-dock click-action`
        * 18.04: `gsettings set org.gnome.shell.extensions.dash-to-dock click-action 'minimize'`
        * https://launchpad.net/ubuntu/+source/gnome-shell-extension-ubuntu-dock
        * ClickAction `minimize-or-previews`: wait for [this commit](https://github.com/micheleg/dash-to-dock/commit/b2e9bb7ca2d92f7e36cda236248913a237525d6a) to be included in a release
    * New text file on right click: `touch ~/Templates/New\ Text\ File.txt`
    * Move apps button to the top: `gsettings set org.gnome.shell.extensions.dash-to-dock show-apps-at-top true`
    * Show apps on Win key press
        * https://extensions.gnome.org/extension/1198/start-overlay-in-application-view/
        * `unzip start-overlay-in-application-view@cis.net.v2.shell-extension.zip -d ~/.local/share/gnome-shell/extensions/start-overlay-in-application-view@cis.net`
        * <kbd>Alt</kbd>+<kbd>F2</kbd>, `r`, <kbd>Enter</kbd>
        * Restart `GNOME Tweak Tool` if it was running, then enable the extension
    * Close the Overview with a single ESC press when searchbox is empty
        * https://extensions.gnome.org/extension/3204/escape-overview/
        * `unzip escape-overviewraelgc.v1.shell-extension.zip -d ~/.local/share/gnome-shell/extensions/escape-overview@raelgc`

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
check out: https://github.com/sdushantha/fontpreview

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
Open Startup Applications (search for "startup app"), click "Add" and under both "Name" and "Command" fields, add "imwheel --kill"
* http://www.webupd8.org/2015/12/how-to-change-mouse-scroll-wheel-speed.html
