## Client installation

**Ubuntu**

The same as server up until `make install`

**Centos**
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
    rotate 4
    size 100k
    daily
    create 0600 root root
}
```
**Cron job**
``` shell
touch /etc/cron.d/burp-client
chmod 600 /etc/cron.d/burp-client
vi /etc/cron.d/burp-client
```
Add the following contents:
```
# Run burp client every 20 minutes
*/20 *    * * * root /usr/sbin/burp -a t >>/var/log/burp-client.log 2>&1
```
Restart cron daemon
``` shell
service crond restart
```
