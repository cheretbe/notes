* `.local/share/icons/hicolor/48x48/apps/4A33_totalcmd64.0.png`
* `.local/share/applications/winbox.desktop`
* http://www.ubuntugeek.com/wl-creator-creates-linux-desktop-launchers-for-windows-programs.html
* https://www.nirsoft.net/utils/iconsext.html

winbox.desktop
```
[Desktop Entry]
Name=Winbox
Exec=env WINEPREFIX="/home/user/.wine" wine C:\\\\windows\\\\command\\\\start.exe /Unix /home/user/.wine/dosdevices/c:/winbox.exe
Type=Application
StartupNotify=true
Comment=c:\winbox.exe
Icon=4A33_totalcmd64.0
StartupWMClass=winbox.exe
```

* `gtk-update-icon-cache` ~~Restart gnome-shell: <kbd>Alt</kbd>+<kbd>F2</kbd>, `restart` or `r`~~
