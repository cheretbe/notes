* Wireplumber
    * view version
      ```
      wireplumber --version
      ``` 
* Wireplumber 0.5+ uses [spa-json](https://pipewire.pages.freedesktop.org/wireplumber/daemon/configuration/conf_file.html#the-spa-json-format) config file, not LUA scripts
    * Migration: https://pipewire.pages.freedesktop.org/wireplumber/daemon/configuration/migration.html
    * https://pipewire.pages.freedesktop.org/wireplumber/daemon/configuration/bluetooth.html
* Old versions use LUA scripts
    * KDE 6.2 has 0.4.17 :(
    * https://web.archive.org/web/20231226224700/https://pipewire.pages.freedesktop.org/wireplumber/
    * https://mazunki.pages.freedesktop.org/wireplumber/configuration/bluetooth.html
    * Device rename example: https://unix.stackexchange.com/questions/648666/rename-devices-in-pipewire/688554#688554

[Outdated] Fix for bluetooth occasionally skipping sound and volume controls not working properly (doesn't apply to recent KDE)

```shell
# as user
systemctl --user --now disable pipewire-media-session

sudo apt purge pipewire-media-session
# Fix for the error:
# Failed to preset unit, file /etc/systemd/user/pipewire-session-manager.service already exists
# and is a symlink to /usr/lib/systemd/user/pipewire-media-session.service.
# https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=997818
sudo rm /etc/systemd/user/pipewire-media-session.service
sudo rm /etc/systemd/user/pipewire-session-manager.service
sudo rm -rf /etc/systemd/user/pipewire.service.wants/

sudo apt install wireplumber libspa-0.2-bluetooth

systemctl --user --now enable wireplumber.service

# [!] reboot

# (Old KDE?) 6.2 has these packages by default
# If device is shown, but can't be connected and there are errors like this in the system log
# a2dp-sink profile connect failed for 41:42:A8:BF:47:78: Protocol not available
apt purge pulseaudio-module-bluetooth
apt install libspa-0.2-bluetooth bluedevil
```

* :warning: https://discourse.ubuntu.com/t/bluetooth-degraded-audio-quality-resolved/27244
* https://wiki.debian.org/BluetoothUser/a2dp
* https://ubuntuhandbook.org/index.php/2022/04/pipewire-replace-pulseaudio-ubuntu-2204/
