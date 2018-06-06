Motherboard and CPU info
```shell
# Motherboard
dmidecode -t 1 -t 2
lshw -class system
# CPU
lscpu
lshw -class processor
cat /proc/cpuinfo
```
CPU stress-test
```shell
sudo apt install stress-ng
nice -19 stress-ng -c 4 --metrics --timeout 5m
```

tracert for Linux
```
apt-get install mtr-tiny
mtr host
```

```shell
# Find file recursively
# -iname:  like -name, but the match is case insensitive
find / -xdev -iname "*sql*"

# Grep the whole filesystem
#  -xdev  Don't descend directories on other filesystems.
# -H, --with-filename  print the file name for each match
find / -xdev -type f -print0 | xargs -0 grep -H "ForceCompositionPipeline"
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

# Set group ID permission
# First change the group on the directory to the one you want to be used as the default:
chgrp group /path/to/directory -R
# Then set the group ID permission on the folder:
chmod g+s /path/to/directory -R
#or
find /path/to/directory -type d -exec chmod chmod g+rwxs {} \;
```

Add user:
``` bash
# adduser is more user friendly and interactive than its back-end useradd
adduser newuser
# On CentOS adduser in not very friendly though
passwd newuser
usermod -aG wheel newuser
# On Ubuntu
adduser newuser sudo
# Disable user login
sudo passwd -l root
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
# Add new group
groupadd group
```

Unsorted
```
tar cvf - directory/ | pigz > /path/to/archive.tar.gz
ssh user@host "cat /path/to/archive.tar.gz" | tar -xzv
tar cvf - /with/full/path | pigz | ssh -p 12345 -i npa_openssh.key user@host "cd /path; tar xzf -"
# Replace identical files by hard links
rdfind -makehardlinks true -removeidentinode true .
```
