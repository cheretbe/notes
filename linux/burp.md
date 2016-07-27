## Client installation

Centos:
``` shell
yum install burp-client
```

Config is in `/etc/burp/burp.conf`

``` shell
touch /etc/logrotate.d/burp-client
```
Add the following contents:
```
/var/log/burp-client.log {
    missingok
    notifempty
    size 30k
    daily
    create 0600 root root
}
```
