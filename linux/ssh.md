## Table of Contents
* [Hardening SSH Access](#hardening-ssh-access)
* [Multiple Instances of sshd](#multiple-instances-of-sshd)
* [Reverse SSH Tunnel](#reverse-ssh-tunnel)
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

Restrict allowed options in `/etc/ssh/sshd_config_rev_tunnel`
```
AllowTcpForwarding yes
X11Forwarding no
PermitTunnel no
#GatewayPorts no
#GatewayPorts clientspecified
GatewayPorts yes
AllowAgentForwarding no
ForceCommand echo 'This service can only be used for reverse port forwarding'
PermitOpen locahost:8844
ClientAliveInterval 60
ClientAliveCountMax 5
```
```bash
# Test tunnel creation
ssh -v -i keys/tunnel-user-key.key tunnel-user@host.domain.tld -p 12345 -N -R 1234:localhost:22
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

## Notes
``` bash
# Find out PIDs of active tunnes
netstat -tulpn | grep sshd
```
`/etc/ssh/sshd_config` options
```apache
# To fix X11 forwading error
X11UseLocalHost no
# Allow port forwading
AllowTcpForwarding yes
```
Do not forward the locale settings
* on client: in `/etc/ssh/ssh_config` comment out the line:
```
SendEnv LANG LC_*
```
* on server: in `/etc/ssh/sshd_config` comment out the line:
```
AcceptEnv LANG LC_*
```
