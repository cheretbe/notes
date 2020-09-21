* https://www.systutorials.com/docs/linux/man/5-autofs.conf/

:warning: for CIFS make sure `cifs-utils` package is installed

options are in `/etc/autofs.conf` on Ubuntu (` /etc/sysconfig/autofs` on RHEL (?))
```
# default is none
logging = debug
```

```shell
# -k, --kerberos                Use kerberos (active directory) authentication
# -d, --debuglevel=DEBUGLEVEL   Set debug level
# -m, --max-protocol=LEVEL      Set the max protocol level
smbclient -L 121-main.gur.local -k -m SMB3 -d 3
```
