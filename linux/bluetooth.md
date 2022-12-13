2review: Fix for bluetooth occasionally skipping sound and volume controls not working properly

```shell
# as user
systemctl --user --now disable pipewire-media-session

# [!!] Check if package name is correct by running apt install -s wireplumber 
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
```

* :warning: https://discourse.ubuntu.com/t/bluetooth-degraded-audio-quality-resolved/27244
* https://ubuntuhandbook.org/index.php/2022/04/pipewire-replace-pulseaudio-ubuntu-2204/
