Creating file systems:
```shell
# ext2
sudo mke2fs /dev/sda1
# ext3
sudo mke2fs -j /dev/sda2
# ext4
sudo mke2fs -t ext4 /dev/sda2
# or
sudo mkfs.ext4 /dev/sda2
```
* `-m 0` – do not reserve space for root
* `-b 1024` – set block size to 1024 (for small files). Default size is 4096. To find out current block size: `sudo tune2fs -l /dev/sdc2`
```shell
# NTFS
# -Q - quick format
sudo sudo mkntfs /dev/sda2 -Q
# Create and use swap:
sudo mkswap /dev/sda3
sudo swapon /dev/sda3
```
/etc/fstab:
```apache
# the last param is pass count (should be 2 for non-root FS to be auto-checked, 0 to disable check)
# optional: _netdev,noatime,user,auto
# blkid or blkid /dev/sda1 to find out UUID
UUID=373be9e0-fc6e-4b4f-b2f3-4b608146bc00 /mnt/mountpoint ext4 defaults 0 2
```
(?) Add new disk without reboot - scsiadd (package scsiadd)
