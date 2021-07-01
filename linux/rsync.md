```shell
# -v increase verbosity
# -r recurse into directories
# -h output numbers in a human-readable format
# -l copy symlinks as symlinks
# -t preserve modification times
rsync -e 'ssh -p 1234 -i /path/to/a/key' \
# --progress \
-vrhlt --delete-excluded --exclude-from rsync_exclude.lst \
root@host.domain.tld :/etc :/home :/root :/usr/local \
/dst/path/

# /src dst[/]   ==> Creates src subdirectory in dst
# /src/ dst[/]  ==> Copies src content to dst itself
# In both cases dst will be created if doesn't exists
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
