```shell
swapoff /swapfile

# Create swap file at least as large as the computer's RAM
dd if=/dev/zero of=/swapfile bs=$(cat /proc/meminfo | awk '/MemTotal/ {print $2}') count=1024 conv=notrunc

mkswap /swapfile
swapon /swapfile

blkid $(df -P / | tail -1 | cut -d' ' -f 1)

filefrag -v /swapfile

# Filesystem type is: ef53
# File size of /swapfile is 16419532800 (4008675 blocks of 4096 bytes)
#  ext:     logical_offset:        physical_offset: length:   expected: flags:
#    0:        0..   63487:      34816..     98303:  63488:
#                                |<------ we need this

nano /etc/default/grub
# Update GRUB_CMDLINE_LINUX_DEFAULT value
# GRUB_CMDLINE_LINUX_DEFAULT="quiet splash resume=UUID=xxx resume_offset=yyy"

update-grub

nano /etc/initramfs-tools/conf.d/resume
RESUME=UUID=xxx resume_offset=yyy

update-initramfs -c -k all

nano /etc/polkit-1/localauthority/50-local.d/com.ubuntu.enable-hibernate.pkla
```
```
[Re-enable hibernate by default in upower]
Identity=unix-user:*
Action=org.freedesktop.upower.hibernate
ResultActive=yes

[Re-enable hibernate by default in logind]
Identity=unix-user:*
Action=org.freedesktop.login1.hibernate;org.freedesktop.login1.handle-hibernate-key;org.freedesktop.login1;org.freedesktop.login1.hibernate-multiple-sessions;org.freedesktop.login1.hibernate-ignore-inhibit
ResultActive=yes
```

```shell
cat /usr/share/gnome/gnome-version.xml

# https://extensions.gnome.org/extension/755/hibernate-status-button/

mkdir -p ~/.local/share/gnome-shell/extensions/
unzip ~/Downloads/hibernate-statusdromi.v33.shell-extension.zip -d ~/.local/share/gnome-shell/extensions/hibernate-status@dromi

apt install gnome-shell-extensions
#Logoff/logon, then run "Extensions" application
```

* https://www.linuxuprising.com/2021/08/how-to-enable-hibernation-on-ubuntu.html
* https://ubuntuhandbook.org/index.php/2021/08/enable-hibernate-ubuntu-21-10/#comments
* https://rephlex.de/blog/2019/12/27/how-to-hibernate-and-resume-from-swap-file-in-ubuntu-20-04-using-full-disk-encryption/
* http://blog.holdenkarau.com/2022/05/making-hibernate-work-on-ubuntu-2204.html
