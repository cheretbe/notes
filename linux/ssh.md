## Hardening SSH Access
SSH daemon options in `/etc/ssh/sshd_config`:
```
PermitRootLogin no
# [!!!] Authentication key-pair must be created and tested beforehand
PasswordAuthentication no
# [!!!] If SELinux is enabled, SSH daemon needs to be allowed to listen on new port
# semanage port -a -t ssh_port_t -p tcp #PORTNUMBER
Port <port_number>
```

## Multiple instances of sshd

### Centos 7 (systemd)

```
ln -s /usr/sbin/sshd /usr/sbin/sshd-external
```

* Make a copy of the systemd unit file for the sshd service
```
cp /usr/lib/systemd/system/sshd{,-external}.service
debian 8
cp /lib/systemd/system/ssh{,-external}.service
```

* Modify `sshd-external.service` file
```
vi /usr/lib/systemd/system/sshd-external.service
debian
vi /lib/systemd/system/ssh-external.service
```
```
# modify Description
Description=OpenSSH server daemon (external)
# modify After: add sshd.service, so that the second instance starts only after the first
# one has started (which includes key generation), remove sshd-keygen.service
After=network.target sshd.service
# modify ExecStart (add -f /etc/ssh/sshd_config_external)
ExecStart=/usr/sbin/sshd-external -D -f /etc/ssh/sshd_config_external $SSHD_OPTS
#debian (check if this is applicable to centos)
[Install]
Alias=sshd-external.service
```

* Make a copy of the sshd_config file 
```
cp /etc/ssh/sshd_config{,_external}
```

* Edit sshd-second_config to assign a different port number and PID file
```
vi /etc/ssh/sshd_config_external
```
```
Port 22220
# Uncomment or add
PidFile /var/run/sshd-external.pid
```

Enable service start on boot
```
systemctl enable sshd-external
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
To fix X11 forwading error add the following line to `/etc/ssh/sshd_config`
```
X11UseLocalHost no
```
