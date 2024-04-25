* :warning: Don't forget `-n`, `--dry-run` option!
* https://serverfault.com/questions/455111/rsynced-files-not-getting-proper-acl
  * try `--chmod=ug=rwX`
* https://stackoverflow.com/questions/667992/rsync-error-failed-to-set-times-on-foo-bar-operation-not-permitted/668049#668049
  * either change owner on target or use `-O`, `--omit-dir-times` in addition to `-t`

`-a --no-specials --no-devices` tells rsync to skip these files (devices, sockets and fifos). It will still print an information message, but it would return 0 if no other error occurs. Useful when copying whole filesystems (search keywords: copy root, copying root). See also [tar](./tar.md) excludes example.

```shell
# -v increase verbosity
# -r recurse into directories
# -h output numbers in a human-readable format
# -l copy symlinks as symlinks
# -t preserve modification times
rsync -e 'ssh -p 1234 -i /path/to/a/key' \
# --delete --progress --checksum \
-vrhlt --delete-excluded --exclude-from rsync_exclude.lst \
root@host.domain.tld :/etc :/home :/root :/usr/local \
/dst/path/

# /src dst[/]   ==> Creates src subdirectory in dst
# /src/ dst[/]  ==> Copies src content to dst itself
# In both cases dst will be created if doesn't exists

# Permissions
# --chmod=Du=rwx,Dg=rwx,Do=,Fu=rw,Fg=rw,Fo=
# or
# --chmod=D0770,F0660
# 
```
rsync_exclude.lst
```
/root/temp/
/home/npa/temp/
```

### Rsync daemon
* https://serverspace.io/support/help/use-rsync-to-create-a-backup-on-ubuntu/
* https://superuser.com/questions/1401490/rsync-password-mismatch-although-it-is-a-scp-copy/1410265#1410265
* https://man7.org/linux/man-pages/man5/rsyncd.conf.5.html

`/etc/rsyncd.conf` example:
```
pid file = /var/run/rsyncd.pid
read only = yes
# Allow local connections only
# address = 127.0.0.1

# Limit hosts
# hosts allow = 127.0.0.1,192.168.0.0/24

[data]
path = /path/to/backup
list = yes
auth users = joe:deny @guest:deny admin:rw @rsync:ro susan joe sam
secrets file = /etc/rsyncd.secrets
```
```shell
chmod 600 /etc/rsyncd.secrets
```
`/etc/rsyncd.secrets` example
```
susan:password
joe:password
```

```shell
cp /lib/systemd/system/rsync.service /etc/systemd/system/rsync.service
systemctl daemon-reload
```
Client call example<br>
:warning: Not that for rsync client password file should contain **only password**, not `username:password`

```shell
rsync -vrhlt --password-file=/etc/rsyncd.passwd backuppc@localhost::smb/172.24.0.11/C/Users dst

# List module contents recursive
rsync user@localhost::home -r
```
