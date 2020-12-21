* https://www.man7.org/linux/man-pages/man5/auto.master.5.html
* https://www.systutorials.com/docs/linux/man/5-autofs.conf/

:warning: for CIFS make sure `cifs-utils` package is installed

`--ghost` option is deprecated, use `[no]browse` instead

options are in `/etc/autofs.conf` on Ubuntu (` /etc/sysconfig/autofs` on RHEL)
```
# default is none
logging = debug
```

`/etc/auto.master` entry example (:warning: use `\$` to escape dollar sign in share name)
```
# unmount after 10 minutes of inactivity, default is 300 seconds (5 minutes)
# browse option pre-creates mount point directories for indirect mount maps so
# the map keys can be seen in a directory listing without being mounted
/mnt/smb /etc/auto.srv-name --timeout=600 -browse
```
`/etc/auto.srv-name` example
```
srv-name -fstype=cifs,credentials=/root/.srv-name_credentials,dir_mode=0755,file_mode=0755,uid=username,rw /share1 ://srv-name.domain.tld/share1 /share2 ://srv-name.domain.tld/share2
```
`/root/.srv-name_credentials` example
```
username=user
password=pwd
domain=DOMAIN
```

```shell
# -k, --kerberos                Use kerberos (active directory) authentication
# -d, --debuglevel=DEBUGLEVEL   Set debug level
# -m, --max-protocol=LEVEL      Set the max protocol level
smbclient -L srv-name.domain.tld -k -m SMB3 -d 3
```
