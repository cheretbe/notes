```shell
# Mount disk image file
# Make sure file is not compressed
file /path/disk.img

# https://unix.stackexchange.com/questions/316401/how-to-mount-a-disk-image-from-the-command-line/316410#316410
fdisk -lu /path/disk.img

# fdisk shows offset in blocks, so note block size and used it like this
mount -o loop,offset=$((514048*512)) /path/disk.img /mnt/loop
```

```shell
# Identify SATA ports of connected drives
# lsscsi package needs to be installed
# look for ataX part (e.g. /sys/devices/pci0000:00/0000:00:1f.2/ata2/host1/target1:0:0/1:0:0:0)
lsscsi --verbose

# Re-read partition table from a drive
partprobe /dev/sdX
```

Clear MBR and partition table
```shell
# 2 blocks of 512 bytes (for GPT)
dd if=/dev/zero of=/dev/sdX bs=512 count=2

# For ZFS metadata at the end of the disk
# https://superuser.com/questions/1248905/how-to-delete-some-zfs-metadata-from-hard-drive
dd if=/dev/zero of=/dev/sdX seek=$(($(blockdev --getsz "/dev/sdX") - 1024))
```
Backup and restore MBR and partition table
```shell
# MBR is 512 bytes long:
# 1 - the boot code (446 bytes)
# 2 - the partition table (64 bytes)
# 3 - the boot code signature (2 bytes)
dd if=/dev/sdX of=sdX_mbr.dat count=1 bs=512
# Save extended partitions information
sfdisk -d /dev/sdX > sdX_partitions.sfdisk

# Restore
# [!] Check disk name
# MBR
dd if=sdX_mbr.dat of=/dev/sdX
# Partitions
# [!!!] Double-check disk name IN THE FILE
sfdisk /dev/sdX < sdX_partitions.sfdisk
```

Frequently used fdisk partition types: swap partition (type 82) linux partition (type 83).

```shell
parted /dev/sda
# change device
(parted) select /dev/sdb
# create GPT partition table
(parted) mklabel gpt
# create DOS partition talbe
(parted) mklabel msdos
# create partition interactively
(parted) mkpart primary
# swap partition type: linux-swap
# create partition using whole disk
# (try start from 1 if it warnings about not proper alignment)
(parted) mkpart primary 0 100%
# other partitions
(parted) mkpart primary 1 25Gb
(parted) mkpart logical 372737 500000
# set boot flag
(parted) set 1 boot on
# mark partition as LVM
(parted) set 1 lvm on

```

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
```shell
# Protect ummounted mount point ([!] when umounted)
# i - immutable: it makes a file immutable, which goes a step beyond simply disabling
# write access to the file. The file can’t be deleted, links to it can’t be created,
# and the file can’t be renamed.
chattr +i /mnt/mountpoint

# View current attributes
# -d     List directories like other files, rather than listing their contents.
lsattr -d /mnt/mountpoint
```

(?) Add new disk without reboot - scsiadd (package scsiadd)
