* `~/.local/share/icons/hicolor/48x48/apps/winbox_100.png`
* `~/.local/share/applications/winbox.desktop`
* http://www.ubuntugeek.com/wl-creator-creates-linux-desktop-launchers-for-windows-programs.html
* https://www.nirsoft.net/utils/iconsext.html
* https://convertico.com/ico-to-png/
* Wrong icon when running: https://ubuntuforums.org/showthread.php?t=2360326
    * Run `xprop WM_CLASS`
    * Set `StartupWMClass` correctly

winbox.desktop
```
[Desktop Entry]
Name=Winbox
Exec=env WINEPREFIX="/home/user/.wine" wine C:\\\\windows\\\\command\\\\start.exe /Unix /home/user/.wine/dosdevices/c:/winbox.exe
Type=Application
StartupNotify=true
Comment=c:\winbox.exe
Icon=winbox_100
StartupWMClass=winbox.exe

[Desktop Action new-window]
Name=New Window
Exec=env WINEPREFIX="/home/user/.wine" wine C:\\\\windows\\\\command\\\\start.exe /Unix /home/npa/.wine/dosdevices/ c:/winbox.exe
```

* `gtk-update-icon-cache` ~~Restart gnome-shell: <kbd>Alt</kbd>+<kbd>F2</kbd>, `restart` or `r`~~

```shell
env LC_ALL=ru_RU.CP1251 wine "C:\Program Files\1Cv77\BIN\1cv7.exe"
env WINEPREFIX="/home/user/.wine" LC_ALL=ru_RU.CP1251 wine C:\\\\windows\\\\command\\\\start.exe /Unix /home/user/.wine/dosdevices/c:/temp/DM/osdm.bat

```
