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
rdfind -makehardlinks true -removeidentinode true .
```
