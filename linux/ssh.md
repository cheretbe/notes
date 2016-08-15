## Multiple instances of sshd

### Centos 7 (systemd)

* Make a copy of the systemd unit file for the sshd service
```
cp /usr/lib/systemd/system/sshd{,-external}.service
```

* Modify `sshd-external.service` file
```
vi /usr/lib/systemd/system/sshd-external.service
```
```
# modify Description
Description=OpenSSH server daemon (external)
# modify After: add sshd.service, so that the second instance starts only after the first
# one has started (which includes key generation), remove sshd-keygen.service
After=network.target sshd.service
# 
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
PidFile /var/run/sshd-external.pid
```

https://access.redhat.com/solutions/1166283
