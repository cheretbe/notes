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
# modify ExecStart
ExecStart=/usr/sbin/sshd-external -D $SSHD_OPTS
# 
```
debian
After=network.target ssh.service

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
PidFile /var/run/sshd-external.pid
```

https://access.redhat.com/solutions/1166283

## Notes
``` bash
# Find out PIDs of active tunnes
netstat -tulpn | grep sshd
```
