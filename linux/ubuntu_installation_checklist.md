TODO:
* http://askubuntu.com/questions/115333/how-do-i-disable-the-sleep-button-on-my-keyboard/115423#115423
* http://www.noobslab.com/p/themes-icons.html
* http://www.webupd8.org/2016/03/mailnag-email-notifier-12-released-with.html
* http://mark.orbum.net/2012/05/14/disabling-dnsmasq-as-your-local-dns-server-in-ubuntu/
--------
```shell
# List the installed (non-relocatable) schemas
gsettings list-schemas
# List keys in a schema
gsettings list-keys org.gnome.shell.extensions.dash-to-dock
# Query the range (or possible values) of a key
gsettings range org.gnome.shell.extensions.dash-to-dock click-action
```
--------
* 18.04/20.04/22.04
    * DNS fix + `apt purge avahi-daemon`? (check if removing avahi-daemon is enough for 18.04.03)
    * Move windows to other monitor: <kbd>Win</kbd>+<kbd>Shift</kbd>+arrows
    * Disable alert sounds: `gsettings set org.gnome.desktop.sound event-sounds false`
    * Themes (use Gnome Tweaks to change `apt install gnome-tweaks`)
        * :point_right: https://github.com/Jannomag/Yaru-Colors
           * extract .zip to a temp dir, then copy `Themes` subdir contents to `~/.themes`
        * https://www.gnome-look.org/p/1207034/
        * https://github.com/valr/awf
        * https://github.com/themix-project/oomox
    * Login screen background: https://ubuntuhandbook.org/index.php/2022/04/login-screen-background-ubuntu-22-04/
        * `./ubuntu-gdm-set-background --gradient vertical \#000099 \#000033`
    * Move the clock: http://frippery.org/extensions/ (Gnome version is in `/usr/share/gnome/gnome-version.xml`)
        * :warning: We need [Frippery Move Clock](https://extensions.gnome.org/extension/2/move-clock/) only, no need to install full GNOME Shell Frippery
            * `cat /usr/share/gnome/gnome-version.xml` 
            * `mkdir -p ~/.local/share/gnome-shell/extensions/`
            * `unzip ~/Downloads/Move_Clockrmy.pobox.com.v22.shell-extension.zip -d ~/.local/share/gnome-shell/extensions/Move_Clock@rmy.pobox.com`
            * <kbd>Alt</kbd>+<kbd>F2</kbd>, `r`, <kbd>Enter</kbd>
            * Restart `GNOME Tweak Tool` if it was running, then enable the extension
            * :warning: 22.04: `apt install gnome-shell-extensions`, then run "Extensions" application
        * Full GNOME Shell Frippery (left here for the reference)
        ```shell
        # tar contains all necessary paths
        cd ~
        tar xzvf ~/Downloads/gnome-shell-frippery-3.32.4.tgz
        ```
        * Restart shell (<kbd>Alt</kbd>+<kbd>F2</kbd>, <kbd>r</kbd>), then use Gnome Tweaks
    * Get rid of the "Window is ready" notification and focus window immediately
        * https://github.com/v-dimitrov/gnome-shell-extension-stealmyfocus/archive/refs/heads/master.zip 
        * :warning: note the **-j** option: `unzip -j ~/Downloads/master.zip -d ~/.local/share/gnome-shell/extensions/focus-my-window@varianto25.com` 
    * Ctrl+Shift setting is in Gnome-tweaks, `Keyboard & Mouse` > `Additional Layout Options`
    * https://itsfoss.com/ubuntu-shortcuts/
    * https://askubuntu.com/questions/1042641/how-to-set-custom-lock-screen-time-in-ubuntu-18-04
    * `2check`: https://askubuntu.com/questions/1048774/disabling-lock-screen-18-04/1064704#1064704
    * Hide mounted devices from Ubuntu Dock: `gsettings set org.gnome.shell.extensions.dash-to-dock show-mounts false`
    * Click to minimize: `gsettings set org.gnome.shell.extensions.dash-to-dock click-action 'minimize-or-previews'`
        * :warning: 22.04 has `focus-minimize-or-previews` 
        * view available actions: `gsettings range org.gnome.shell.extensions.dash-to-dock click-action` (default for 20.04 is `focus-or-previews`)
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
        * `unzip escape-overviewraelgc.v4.shell-extension.zip -d ~/.local/share/gnome-shell/extensions/escape-overview@raelgc`


- [ ] grub settings
- [ ] NVIDIA driver (Software & Updates -> Additional Drivers)
- [ ] Keyboard settings (use different layout for each window: `Settings` > `Region and Language` > `Input Sources`, gear on the right)
- [ ] `apt install gparted mc htop`
- [ ] Screensaver and lock settings
- [ ] PCManFM
- [ ] Latest Remmina client
```shell
# as root
pkill remmina
apt purge remmina
snap install remmina
```
```bash
# Remmina will no longer be available as a PPA package after the release of version 1.4.8.
# sudo add-apt-repository ppa:remmina-ppa-team/remmina-next
```
- [ ] Change time from UTC to local (when dual-booting with Windows)
```bash
timedatectl set-local-rtc 1
# turn UTC back on
timedatectl set-local-rtc 0
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
```shell
cp /usr/share/applications/org.gnome.Terminal.desktop ~/.local/share/applications/custom-gnome-terminal.desktop
```
  TryExec is used to determine if the program is actually installed. If the file is not present or if it is not executable, the entry may be ignored (not be used in menus, for example). It does not actually execute it's own value. 

  use `--geometry=WxH+X+Y` to set an exact window position (use `xwininfo` to find out current position and geometry)
 ```diff
 [Desktop Entry]
 # VERSION=3.36.2
-Name=Terminal
+Name=Custom Terminal
 Comment=Use the command line
 Keywords=shell;prompt;command;commandline;cmd;
 TryExec=gnome-terminal
-Exec=gnome-terminal
+Exec=gnome-terminal --class=CustomTerminal --geometry 127x43+490+290
+StartupWMClass=CustomTerminal
 Icon=org.gnome.Terminal
 Type=Application
 Categories=GNOME;GTK;System;TerminalEmulator;
 StartupNotify=true
 X-GNOME-SingleWindow=false
 OnlyShowIn=GNOME;Unity;
-Actions=new-window;preferences;
-X-Ubuntu-Gettext-Domain=gnome-terminal
+Actions=new-window
+X-Ubuntu-Gettext-Domain=custom-gnome-terminal

 [Desktop Action new-window]
 Name=New Window
-Exec=gnome-terminal --window
-
-[Desktop Action preferences]
-Name=Preferences
-Exec=gnome-terminal --preferences
+Exec=gnome-terminal --window --class=CustomTerminal
```
  Old version   
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
