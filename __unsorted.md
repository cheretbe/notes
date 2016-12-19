
PCManFM file manager
```
dpkg-reconfigure locales
LANG="ru_RU.CP1251" wine Downloads/bvssol.exe
```

Ubuntu global .desktop files location: `/usr/share/applications`

http://www.windowscentral.com/how-create-windows-10-iso-file-using-installesd-image

http://askubuntu.com/questions/133384/keyboard-shortcut-gnome-terminal-ctrl-tab-and-ctrl-shift-tab-in-12-04/837629#837629
```
gsettings set \
  org.gnome.Terminal.Legacy.Keybindings:/org/gnome/terminal/legacy/keybindings/ \
  next-tab '<Primary>Tab'
gsettings set \
  org.gnome.Terminal.Legacy.Keybindings:/org/gnome/terminal/legacy/keybindings/ \
  prev-tab '<Primary><Shift>Tab'
```

``` bash
# /etc/dhcp/dhclient.conf
# supersede domain-name-servers 8.8.8.8, 8.8.4.4;
dhclient -x
dhclient
```

```
PS C:\Users\Администратор.GUR> Get-WinEvent -ListLog * -EA silentlycontinue | where-object { $_.recordcount -AND $_.last
writetime -gt [datetime]::today} | foreach-object { get-winevent -FilterHashtable @{logname=$_.logname; starttime=((Get-
Date) - (New-TimeSpan -Minutes 10))} -EA SilentlyContinue} | Format-List | Out-String -Stream -width 4096 | Out-File 'C:
\temp\events.txt' -Width 4096
```
