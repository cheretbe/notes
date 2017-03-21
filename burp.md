## Notes

Mailing list:

* [Bare-metal Windows 2008 R2 restore with secure key storage & without a Windows install disc](https://sourceforge.net/p/burp/mailman/message/35612245/)
* [burp server automated](https://sourceforge.net/p/burp/mailman/message/35605032/)
* [Incompatibility between 2.0.54 client and 1.3.48 server](https://sourceforge.net/p/burp/mailman/message/35648448/)
* [Small things after server upgrade](https://sourceforge.net/p/burp/mailman/message/35653928/)
* [parameters/variables for use in pre/post scripts](https://sourceforge.net/p/burp/mailman/message/35671910/)

The status monitor is now a client-side operation.
Please read http://burp.grke.org/docs/monitor.html and you will find out how
to make it work.

```
burp -c /etc/burp/burp-server.conf -t -C testclient | grep timer
```

* https://github.com/grke/burp/wiki/Automated-deploy-and-maintenance

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
