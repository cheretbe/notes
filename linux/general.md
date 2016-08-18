Add user:
```
# adduser is more user friendly and interactive than its back-end useradd
adduser newuser
# On CentOS adduser in not very friendly though
passwd newuser
usermod -aG wheel newuser
# On Ubuntu
adduser newuser sudo
```
Delete user:
```
userdel username
# To delete user's home directory along with the user account itself (includes mail spool /var/mail/username)
userdel -r username
```
