```shell
# Passwordless sudo
echo '%sudo ALL=(ALL:ALL) NOPASSWD:ALL' > /etc/sudoers.d/00_passwordless_sudo
chmod 0440 /etc/sudoers.d/00_passwordless_sudo
```

### Rule matching debug

Create `/etc/sudo.conf` with the following content:
```
Debug sudo /var/log/sudo_debug.log all@debug
Debug sudoers.so /var/log/sudo_debug.log all@debug
```
:warning: Don't forget to remove it after debug, it's very verbose
