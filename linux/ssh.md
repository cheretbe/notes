## Multiple instances of sshd

### systemd (Centos 7, Ubuntu 16.04)

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
