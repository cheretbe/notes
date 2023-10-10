```shell
# Passwordless sudo
# sets correct attributes (0440)
echo '%sudo ALL=(ALL:ALL) NOPASSWD:ALL' | sudo EDITOR='tee' visudo -f /etc/sudoers.d/00_passwordless_sudo
# Configure sudo to keep SSH_AUTH_SOCK
echo 'Defaults    env_keep+=SSH_AUTH_SOCK' | sudo EDITOR='tee' visudo -f /etc/sudoers.d/ssh_auth_sock

# old version
echo '%sudo ALL=(ALL:ALL) NOPASSWD:ALL' > /etc/sudoers.d/00_passwordless_sudo
chmod 0440 /etc/sudoers.d/00_passwordless_sudo
```

```shell
# keep X11 display after sudo
sudo -i
# [!!] change ~username to actual user name
xauth add $(xauth -f ~username/.Xauthority list | tail -1)
```

### Rule matching debug

Create `/etc/sudo.conf` with the following content:
```
Debug sudo /var/log/sudo_debug.log all@debug
Debug sudoers.so /var/log/sudo_debug.log all@debug
```
:warning: Don't forget to remove it after debug, it's very verbose
