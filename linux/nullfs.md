* https://github.com/abbbi/nullfsvfs/
* https://github.com/abbbi/nullfsvfs/issues/15

```shell
mount none /mnt/nullfs -t nullfs

time rsync -vrhlt /smb/172.24.0.11/C /mnt/nullfs
```
