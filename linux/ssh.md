## Table of Contents
* [Hardening SSH Access](#hardening-ssh-access)
* [Multiple Instances of sshd](#multiple-instances-of-sshd)
* [Reverse SSH Tunnel](#reverse-ssh-tunnel)
* [SSH Keys](#ssh-keys)
* [Mount a remote SSH directory](#mount-a-remote-ssh-directory)
* [Notes](#notes)

## Hardening SSH Access
SSH daemon options in `/etc/ssh/sshd_config`:
```
PermitRootLogin no
# [!!!] Authentication key-pair must be created and tested beforehand
PasswordAuthentication no
# [!!!] If SELinux is enabled, SSH daemon needs to be allowed to listen on a new port
# semanage port -a -t ssh_port_t -p tcp #PORTNUMBER
Port <port_number>
```

### Reverse SSH Tunnel

#### On server
Create [an additional instance](#multiple-instances-of-sshd) of sshd. Restrict allowed options in `/etc/ssh/sshd_config_rev_tunnel`
```
AllowTcpForwarding yes
X11Forwarding no
PermitTunnel no
#GatewayPorts no
#GatewayPorts clientspecified
GatewayPorts yes
AllowAgentForwarding no
ForceCommand echo 'This service can only be used for reverse port forwarding'
# PermitOpen locahost:1234
PermitOpen "locahost:1234" "localhost:8765" ssh-ed25519 AAAAC3NzaC1lZDI1NT...
ClientAliveInterval 60
ClientAliveCountMax 5
```
* https://en.wikibooks.org/wiki/OpenSSH/Cookbook/Tunnels
#### On client
```bash
# Test tunnel creation
ssh -v -i keys/tunnel-user-key.key tunnel-user@host.domain.tld -p 12345 -N -R 1234:localhost:22
```

Install `supervisord` and create `/etc/supervisor/conf.d/reverse-ssh-tunnel.conf` file with the following contents
```ini
[program:reverse-ssh-tunnel]
environment=AUTOSSH_GATETIME=0

# -M 0  monitoring port (do not monitor)
# -N    do not execute a remote command, just forward ports
# -T    disable pseudo-tty allocation
# -v    verbose mode
# Additional parameters are in /home/local-user/.ssh/config (remote-tunnel)
command=/usr/bin/autossh -v -M 0 -N -T remote-tunnel

user=local-user
autostart=true
autorestart=true
stderr_logfile=/var/log/supervisor/reverse-ssh-tunnel.log
stdout_logfile=/var/log/supervisor/reverse-ssh-tunnel.log
logfile_maxbytes=50MB
logfile_backups=3
```

`/home/local-user/.ssh/config` contents
```
Host remote-tunnel
  Hostname               host.domain.tld
  ServerAliveInterval    30
  ServerAliveCountMax    3
  PubkeyAuthentication   yes
  PasswordAuthentication no
  ExitOnForwardFailure   yes
  IdentityFile           /home/local-user/keys/tunnel-user-key.key
  User                   tunnel-user
  Port                   12345
  RemoteForward          1234 localhost:22
  RemoteForward          1235 192.168.1.8:443
  ServerAliveInterval    30
  ServerAliveCountMax    3
```
```bash
# Enable and start supervisord service
systemctl enable supervisor.service
service supervisor start

# Reverse tunnel service control
supervisorctl stop reverse-ssh-tunnel
supervisorctl start reverse-ssh-tunnel

# Re-read changed config and restart the service without affecting other services
supervisorctl reread
supervisorctl update
```


## Multiple instances of sshd

### Systemd (Centos 7, Debian 8, Ubuntu 16.04)

```
ln -s /usr/sbin/sshd /usr/sbin/sshd-external
```

* Make a copy of the systemd unit file for the sshd service
```shell
cp /usr/lib/systemd/system/sshd{,-external}.service
# debian/ubuntu
cp /lib/systemd/system/ssh{,-external}.service
```

* Modify `sshd-external.service` file
```shell
vi /usr/lib/systemd/system/sshd-external.service
# debian/ubuntu
vi /lib/systemd/system/ssh-external.service
```
```apache
# modify Description
Description=OpenSSH server daemon (external)
# modify After: add sshd.service, so that the second instance starts only after the first
# one has started (which includes key generation), remove sshd-keygen.service
After=network.target sshd.service
# modify ExecStart (add -f /etc/ssh/sshd_config_external)
ExecStart=/usr/sbin/sshd-external -D -f /etc/ssh/sshd_config_external $SSHD_OPTS

# debian/ubuntu only
[Install]
Alias=sshd-external.service
```

* Make a copy of the sshd_config file 
```
cp /etc/ssh/sshd_config{,_external}
```

* Edit 'sshd_config_external' to assign a different port number and PID file
```
vi /etc/ssh/sshd_config_external
```
```
Port 22220
# Uncomment or add
PidFile /var/run/sshd-external.pid
```

If login fails with `fatal: Access denied for user username by PAM account configuration [preauth]` message, make a copy of the PAM configuation file
```
cp /etc/pam.d/sshd{,-external}
```

Enable service start on boot
```shell
systemctl enable sshd-external
# debian/ubuntu
systemctl enable ssh-external
```

Turn on debugging if daemon fails to load
Add `-ddd` option to `/etc/sysconfig/sshd` (debian `/etc/default/ssh`)
```
SSHD_OPTS=-ddd
```

Re-read systemctl configuration if .service file is modified after start attempt
```
systemctl daemon-reload
```

https://access.redhat.com/solutions/1166283

## SSH Keys

```shell
# Generate a key (by default key size is 2048, which is fine). It seems that for RSA (not RSA1) keys comment is
# only added to the test.key.pub file, not to the key itself, so it can be skipped altogether
ssh-keygen -C "test-comment" -f test.key
# View the fingerprint
ssh-keygen -lf key_file
# Retrieve the public key
ssh-keygen -yf key_file
```
To add a comment in `authorized_keys` just use a space and a comment after the key:
```
ssh-dss AAAAB3N...JjHIvNsBk= ThisIsAComment
```

* https://wiki.archlinux.org/index.php/SSH_keys#Choosing_the_authentication_key_type

## Mount a remote SSH directory
```shell
sudo apt install sshfs
# Create the mount point
mkdir ~/yourmountdirectory
# Mount remote path
sshfs username@host:/remotepath ~/yourmountdirectory
# Unmount
fusermount -u ~/yourmountdirectory
```

## Notes
Custom connection options
```
touch ~/.ssh/config
```
```
Host host1
  HostName host1.domain.tld
  User username
  Port 1234
  IdentityFile /path/to/a/file
  ForwardX11 yes
  LocalForward 2345 192.168.0.1:3389
  StrictHostKeyChecking no
  UserKnownHostsFile /dev/null
  ServerAliveInterval    30
  ServerAliveCountMax    3
```


```bash
# RDP port forwarding
ssh user@host.tld -L 1234:192.168.0.200:3389
# Don't check host key and don't add it to known_hosts
ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null user@host.tld
```

``` bash
# Find out PIDs of active tunnels
netstat -tulpn | grep sshd
```
`/etc/ssh/sshd_config` options
```apache
# To fix X11 forwading error
X11UseLocalHost no
# Allow port forwading
AllowTcpForwarding yes
```
```shell
# Keeping X11 display after su or sudo
# For non-root accounts list authority file contents BEFORE su
xauth -f ~/.Xauthority list
# Note the last line, e.g:
# host.domain.tld:10  MIT-MAGIC-COOKIE-1  75260434b52f448f9e21e0cf8c694102
# After su add the same entry for a new user
xauth add host.domain.tld:10  MIT-MAGIC-COOKIE-1  75260434b52f448f9e21e0cf8c694102

# For root the following one-liner is enough
xauth add $(xauth -f ~john/.Xauthority list|tail -1)
```
Do not forward the locale settings
* on client: in `/etc/ssh/ssh_config` comment out the line:
```
#SendEnv LANG LC_*
```
Can't be disabled in `~/.ssh/config` (https://superuser.com/questions/485569/how-to-disable-sendenv-variables-set-in-ssh-config-from-ssh-config)

* on server: in `/etc/ssh/sshd_config` comment out the line:
```
#AcceptEnv LANG LC_*
```
