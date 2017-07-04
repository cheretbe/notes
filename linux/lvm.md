
> Even if LVM itself doesn't care about having a real partition, one reason to create it anyway
> is to inform partitioning programs that there's "something there."
> A nightmare scenario is a new sysadmin diagnosing a boot problem on a server,
> firing up a partitioning program, seeing unpartitioned disks, and concluding that the drive is corrupt.
* https://serverfault.com/questions/439022/does-lvm-need-a-partition-table/439026#439026

parted
```
mklabel gpt
mkpart primary 1M 100%
set 1 lvm on
```

```shell
apt install lvm2

pvcreate /dev/sdb1 [/dev/sdc1]
pvdisplay


```
