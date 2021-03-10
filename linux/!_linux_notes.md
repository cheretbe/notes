HEIC to JPG
```shell
for i in *.heic; do ffmpeg -i "$i" "${i%.*}.jpg"; done
```

Motherboard and CPU info
```shell
# Motherboard
dmidecode -t 1 -t 2
lshw -class system
# CPU
lscpu
lshw -class processor
cat /proc/cpuinfo
# Memory
dmidecode -t memory
dmidecode -t 16
lshw -class memory
dmidecode -t memory | grep Size
```
CPU stress-test
```shell
sudo apt install stress-ng
nice -19 stress-ng -c 4 --metrics-brief --timeout 5m
```

tracert for Linux
```
apt-get install mtr-tiny
mtr host
```
fsck with progress
```
sudo fsck -C -V /dev/sdbX
```

```shell
# Find file recursively
# -iname:  like -name, but the match is case insensitive
find / -xdev -iname "*sql*"

# Grep the whole filesystem
# -xdev  Don't descend directories on other filesystems.
# -H, --with-filename  print the file name for each match
# -I  equivalent to --binary-files=without-match
find / -xdev -type f -print0 | xargs -0 grep -H -I "ForceCompositionPipeline"
# -m 1 to return only the first match
```

Find all hardlinks to a file
```shell
find . -samefile /path/to/file 
```

Fix for ncdu drawing characters in PuTTY
```shell
export NCURSES_NO_UTF8_ACS=1
# Set permanently
echo export NCURSES_NO_UTF8_ACS=1 >> ~/.bashrc
```

Permissions:
```bash
# r=4, w=2, x=1
# + and - signs also can be used: user (u), owner group (g), others (o), and all users (a)
# Default permissions: 644 (rw-r--r--) for a file and 755 (rwxr-xr-x) for a directory
# Set permissions recursively
find . -type f -exec chmod 644 {} \;
find . -type d -exec chmod 755 {} \;

# List permissions as octal numbers
# -c  --format=FORMAT
#           use  the  specified  FORMAT instead of the default; output a newline after
#           each use of FORMAT
# %A     access rights in human readable form
# %a     Access rights in octal
# %n     File name
stat -c '%A %a %n' /home/*

# Set group ID permission
# First change the group on the directory to the one you want to be used as the default:
chgrp group /path/to/directory -R
# Then set the group ID permission on the folder:
chmod g+s /path/to/directory -R
#or
find /path/to/directory -type d -exec chmod chmod g+rwxs {} \;
```
```
Umask   Created Files       Created Directories
-------------------------------------------------
000     666 (rw-rw-rw-)     777     (rwxrwxrwx)
002     664 (rw-rw-r--)     775     (rwxrwxr-x)
022     644 (rw-r--r--)     755     (rwxr-xr-x)
027     640 (rw-r-----)     750     (rwxr-x---)
077     600 (rw-------)     700     (rwx------)
277     400 (r--------)     500     (r-x------)
```

Add user:
``` bash
# adduser is more user friendly and interactive than its back-end useradd
adduser newuser
# On CentOS adduser is not very friendly though
passwd newuser
usermod -aG wheel newuser
# On Ubuntu
adduser newuser sudo
# Disable user login
sudo passwd -l root
# Check if password is locked
# L: locked password, NP: no password, P: usable password
passwd -S [user]
```
Delete user:
``` bash
userdel username
# To delete user's home directory along with the user account itself (includes mail spool /var/mail/username)
userdel -r username
```
Group membership
``` bash
# List all members of a group
getent group <group-name>
# Check a user's group membership
groups [username]
# Add to multiple groups
usermod -a -G group1,group2 username
# For current user
# [!] Make sure not run this as root
sudo usermod -aG group1,group2 ${USER}
# Add new group
groupadd group
# Delete user from a group
gpasswd -d user group
# Delete group
groupdel group-name
```
Sudo

```
# <user list> <host list> = <operator list> <tag list> <command list>

# Allow user execute any command without entering password
username ALL=(ALL) NOPASSWD: ALL
# Allow group execute any command without entering password
%group1	ALL=(ALL) NOPASSWD: ALL
```
* https://help.ubuntu.com/community/Sudoers

Unsorted
```
# Replace identical files by hard links
rdfind -makehardlinks true -removeidentinode true .
```
