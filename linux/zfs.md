* https://wiki.archlinux.org/index.php/ZFS
* https://icesquare.com/wordpress/how-to-improve-zfs-performance/
* https://github.com/zfsonlinux/zfs/wiki/Ubuntu-16.04-Root-on-ZFS

for sda1:
```
parted -- /dev/sda mklabel msdos Y mkpart primary zfs 0% 100%
```

### 1. Installation
For Ubuntu 15.10+ ZFS packages are provided by the distribution
```
apt install zfs
```

14.04:
```
add-apt-repository ppa:zfs-native/stable
apt-get update
apt-get install ubuntu-zfs
```

### 2. Memory tuning
`/etc/modprobe.d/zfs.conf` – may be needed in Linux, since ZFS ARC (Advanced Replacement Cache) can release memory with a delay. If the machine is a dedicated file server, this setting may not be needed
```
# value is in bytes!
# 16GB=17179869184, 8GB=8589934592, 4GB=4294967296, 2GB=2147483648, 1GB=1073741824
options zfs zfs_arc_max=4294967296
```
Check current in-use value:
```
sudo grep c_max /proc/spl/kstat/zfs/arcstats
```
Source: http://arstechnica.com/information-technology/2014/02/ars-walkthrough-using-the-zfs-next-gen-filesystem-on-linux/

### 3. Create zpool
```
zpool create -f -o ashift=12 -O atime=off zfs-storage raidz1 /dev/disk/by-id/ata-ST1000NM0011_Z1N1VTW3 …
```
* **-o ashift=12** uses 4K blocks instead of 512K (this increases performance especially on large disks)
* **-O atime=off** Disables access time updates
* **-f** option forces creation on errors (like existing data on disk etc.)
* **-m /mnt/mountpoint** sets mountpoint location instead of /poolname
### 4. Useful ZFS commands
```shell
zpool status
zfs list
zfs create zfs-storage/share
zfs create zfs-storage/compressed

# enable ACL
zfs set acltype=posixacl <dataset>
# turn compression on
zfs set compression=on zfs-storage/compressed
# check dataset
zpool scrub zfs-storage
# turn on deduplication
zfs set dedup=on zfs-storage/withdedup
# remove dataset
zfs destroy zfs-storage/share
```
### 5. Set up health monitoring script
Download script from https://calomel.org/zfs_health_check_script.html, save to `/etc/cron.daily/zfs_health_check` (do not use .sh extension as dot breaks anacron functionality) and modify it to use with Ubuntu:
```bash
#! /usr/local/bin/bash
#!/bin/bash
...
# Comment out FreeBSD date format and uncomment Ubuntu one
    ### FreeBSD with *nix supported date format
    # scrubRawDate=$(/sbin/zpool status $volume | grep scrub | awk '{print $15 $12 $13}')
    # scrubDate=$(date -j -f '%Y%b%e-%H%M%S' $scrubRawDate'-000000' +%s)

    ### Ubuntu with GNU supported date format
    scrubRawDate=$(/sbin/zpool status $volume | grep scrub | awk '{print $11" "$12" " $13" " $14" "$15}')
    scrubDate=$(date -d "$scrubRawDate" +%s)
```
Check if script works:
```shell
chmod 755 /etc/cron.daily/zfs_health_check
# temporarily shift current date for 9 days to trigger
# scrub expiration message (max scrub age is 8 days by default)
service ntp stop
date --set="$(date) + 9 days"
/etc/cron.daily/zfs_health_check.sh
ntpdate -s ru.pool.ntp.org
service ntp start
```
Add weekly integrity check to `/etc/crontab`:
```
# every sunday at 4:00
0 4 * * 0 root /sbin/zpool scrub zfs-data
```

### 6. Replace a disk in a pool
Replacing `/dev/disk/by-id/ata-VBOX_HARDDISK_sn002` -> `/dev/disk/by-id/ata-VBOX_HARDDISK_sn111`
* Planned
```bash
zpool offline zfs-data /dev/disk/by-id/ata-VBOX_HARDDISK_sn002
# Replace disks
zpool replace -f zfs-data /dev/disk/by-id/ata-VBOX_HARDDISK_sn002 /dev/disk/by-id/ata-VBOX_HARDDISK_sn111
# View progress
zpool status
```
* Unplanned (disk is completely dead and has already been removed)
```bash
# Find out disk's GUID
zdb
# GUID is 16718377149670207017
zpool offline zfs-data 16718377149670207017
zpool replace -f zfs-data 16718377149670207017 /dev/disk/by-id/ata-VBOX_HARDDISK_sn111
# View progress
zpool status
```
