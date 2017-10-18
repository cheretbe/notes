```shell
rsync -e 'ssh -p 1234 -i /path/to/a/key' \
-vrhlt --delete-excluded --exclude-from rsync_exclude.lst \
root@host.domain.tld :/etc/ :/home/ :/root/ :/usr/local/ \
/dst/path/
```
