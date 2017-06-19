* [!] Check difference between `split_vss` and `strip_vss`
* https://sourceforge.net/p/burp/mailman/message/35060752/ (more on this in burp-ui docs)

## Notes

Mailing [list](https://sourceforge.net/p/burp/mailman/burp-users/):

* [Bare-metal Windows 2008 R2 restore with secure key storage & without a Windows install disc](https://sourceforge.net/p/burp/mailman/message/35612245/)
* [burp server automated](https://sourceforge.net/p/burp/mailman/message/35605032/)
* [Incompatibility between 2.0.54 client and 1.3.48 server](https://sourceforge.net/p/burp/mailman/message/35648448/)
* [Small things after server upgrade](https://sourceforge.net/p/burp/mailman/message/35653928/)
* [parameters/variables for use in pre/post scripts](https://sourceforge.net/p/burp/mailman/message/35671910/)
* [Burp with samba](https://sourceforge.net/p/burp/mailman/message/35769281/)
* [fail2ban filter for burp](https://sourceforge.net/p/burp/mailman/message/35786582/)
* [Remove colon in backups](https://sourceforge.net/p/burp/mailman/message/35535192/)

The status monitor is now a client-side operation.
Please read http://burp.grke.org/docs/monitor.html and you will find out how
to make it work.

```
burp -c /etc/burp/burp-server.conf -t -C testclient | grep timer
```

* https://github.com/grke/burp/wiki/Automated-deploy-and-maintenance

## Client

**Windows**
Silent install:
```
burp-win64-installer-2.0.54.exe /S
```
```batch
:: Scheduled task
schtasks /query /tn "burp cron"
schtasks /change /disable /tn "burp cron"
schtasks /change /enable /tn "burp cron"
schtasks /run /tn "burp cron"
schtasks /end /tn "burp cron"
```
**Ubuntu**

* https://ziirish.info/repos/README.txt
```shell
# 16.04
cat >/etc/apt/sources.list.d/ziirish.list<<EOF
deb http://ziirish.info/repos/ubuntu/xenial zi-stable main
EOF

wget http://ziirish.info/repos/ubuntu.gpg -O- | sudo apt-key add -
apt update
apt install burp-core burp-client
# Both burp-server and burp-client can be installed on the same host
apt install burp-server
```

~~The same as server up until `make install`~~

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

## Server config
`cp /etc/burp/burp-server.conf{,.bak}`
```
# default is /var/spool/burp
directory = /path/to/dir
hardlinked_archive = 1
# To use ZFS compression
compression = 0

# Allow backups 24/7
timer_arg = Mon,Tue,Wed,Thu,Fri,Sat,Sun,00,01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,20,21,22,23

# set after debug
notify_success_warnings_only = 1
notify_success_arg = To: notifications@rs-kgr.local
notify_failure_arg = To: notifications@rs-kgr.local

# other params
# max_children = 5
# Check if the following works
#syslog = 0
#logfile=/var/log/burp/burp-server.log
```
Auto upgrade

```
# burp-server.conf
autoupgrade_dir = /etc/burp/autoupgrade/server
# client config
# [!] on client side, not in /etc/burp/clientconfdir
autoupgrade_os = win64
autoupgrade_dir = C:/Program Files/Burp/autoupgrade
```

Examples of "script" files are given in the **source package**, in `configs/server/autoupgrade`

```shell
cd ~/temp
git clone https://github.com/grke/burp.git
cp burp/configs/server/autoupgrade/windows.script /etc/burp/autoupgrade/server/win32/script
cp burp/configs/server/autoupgrade/windows.script /etc/burp/autoupgrade/server/win64/script
```

Put installer into `/etc/burp/autoupgrade/server/<os>/<version>` and rename it into `package`. For example, for version 2.0.54:
* burp-win32-installer-2.0.54.exe => /etc/burp/autoupgrade/server/win32/2.0.54/package
* burp-win64-installer-2.0.54.exe => /etc/burp/autoupgrade/server/win64/2.0.54/package
