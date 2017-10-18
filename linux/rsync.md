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
```
rsync_exclude.lst
```
/root/temp/
/home/npa/temp/
```
