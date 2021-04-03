* 2read
    * https://www.delphix.com/blog/delphix-engineering/zfs-raidz-stripe-width-or-how-i-learned-stop-worrying-and-love-raidz
    * http://www.openoid.net/zfs-practicing-failures/
    * https://calomel.org/zfs_raid_speed_capacity.html

:warning: Clear ZFS metadata at the end(!) of a disk
```shell
# https://superuser.com/questions/1248905/how-to-delete-some-zfs-metadata-from-hard-drive
dd if=/dev/zero of=/dev/sda seek=$(($(blockdev --getsz "/dev/sda") - 1024))
```

## Table of Contents
* [Installation](#installation)
* [zpool Creation](#zpool-creation)
* [Performance Tuning](#performance-tuning)
* [Useful ZFS Commands](#useful-zfs-commands)
* [Health Monitoring Script](#health-monitoring-script)
* [Move single disk file system to another drive](#move-single-disk-file-system-to-another-drive)
* [Replace a Disk in a Pool](#replace-a-disk-in-a-pool)
* [Send Over SSH or netcat](#send-over-ssh-or-netcat)
* [Raspberry Pi](#raspberry-pi)
* [Unsorted](#unsorted)

### Installation
For Ubuntu 15.10+ ZFS packages are provided by the distribution
```shell
apt install zfs
# 18.04
apt install zfsutils-linux
```

14.04:
```
add-apt-repository ppa:zfs-native/stable
apt-get update
apt-get install ubuntu-zfs
```
CentOS
```shell
# 7.3
yum install http://download.zfsonlinux.org/epel/zfs-release.el7_3.noarch.rpm
gpg --quiet --with-fingerprint /etc/pki/rpm-gpg/RPM-GPG-KEY-zfsonlinux

# By default DKMS version is installed (implies compilation)
# For kABI-tracking kmod version (will work with the distribution
# provided kernel only) edit /etc/yum.repos.d/zfs.repo file
# set enabled=0 in [zfs] section
# set enabled=1 in [zfs-kmod] section
yum install kernel-devel zfs
modprobe zfs

# If zfs module is not loaded during the boot, check services enabled status
systemctl is-enabled zfs-import-cache zfs-import-scan zfs-mount zfs-share zfs-zed zfs.target
# If not enabled
systemctl preset zfs-import-cache zfs-import-scan zfs-mount zfs-share zfs-zed zfs.target
#  zfs-import-scan might still be disabled
systemctl enable zfs-import-scan
```
* https://github.com/zfsonlinux/zfs/wiki/RHEL-%26-CentOS

* [\[ TOC \]](#table-of-contents)

### zpool Creation
```shell
# If not using the whole device partition type is zfs
parted -- /dev/sda mklabel msdos Y mkpart primary zfs 0% 100%

# -o property=value               Sets the given pool properties
# -O file-system-property=value   Sets the given file system properties in the root file system of the pool
# [!] consider compression: -o feature@lz4_compress=enabled and -O compression=lz4
zpool create -o ashift=12 -o feature@lz4_compress=enabled -O xattr=sa -O atime=off -O compression=lz4 -O acltype=posixacl zfs-storage raidz1 /dev/disk/by-id/ata-ST1000NM0011_Z1N1VTW3 ...
# Mirrored
zpool create pool1 mirror /dev/vda /dev/vdb
```
* **-f** option forces creation on errors (like existing data on disk etc.)
* **-O xattr=sa** stores xattr as system attributes (increases performance on Linux, not portable to other platforms)
    * https://github.com/zfsonlinux/zfs/issues/443
    * https://www.reddit.com/r/zfs/comments/89xe9u/zol_xattrsa/
* **-o ashift=12** uses 4K blocks instead of 512K (this increases performance especially on large disks)
    * It's a bit shift value, 512 bytes is 9 (2^9 = 512), 4096 bytes is 12 (2^12 = 4096)
    * https://github.com/zfsonlinux/zfs/wiki/faq#advanced-format-disks
    * https://habr.com/post/314506/
    * https://github.com/zfsonlinux/zfs/blob/master/cmd/zpool/zpool_vdev.c#L107
* **-O atime=off** Disables access time updates
* **-m /mnt/mountpoint** sets mountpoint location instead of /poolname
* **-o feature@lz4_compress=enabled** by default (`-o compression=on`) it's either `lzjb` or `lz4` (if `lz4_compress` feature is enabled)
    * https://github.com/zfsonlinux/zfs/blob/master/man/man8/zfs.8 search for `default compression`
* **-O compression=lz4**
    * Use `lz4` for compressed/mixed/unknown data
    * https://www.servethehome.com/the-case-for-using-zfs-compression/

Change mount point after creation
```shell
zfs set mountpoint=/mountpoint pool/filesystem
```
View current values
```shell
# ashift
zdb -CC [pool]
# for non-imported pool
zdb -CC -e pool

zfs get xattr pool
zfs get atime pool
zfs get mountpoint pool

# lz4_compress
zpool get all [pool] | grep 'feature@lz4_compress'
# or
zpool get feature@lz4_compress [pool]
```
* [\[ TOC \]](#table-of-contents)

### Performance Tuning
##### Memory
`/etc/modprobe.d/zfs.conf` – may be needed in Linux, since ZFS ARC (Advanced Replacement Cache) can release memory with a delay. If the machine is a dedicated file server, this setting may not be needed.<br>
:warning: Not anymore. By default now it uses 50% of memory, not 3/4 (https://github.com/zfsonlinux/zfs/wiki/ZFS-on-Linux-Module-Parameters#zfs_arc_max)
```
# value is in bytes!
# 16GB=17179869184, 8GB=8589934592, 4GB=4294967296, 2GB=2147483648, 1GB=1073741824
options zfs zfs_arc_max=4294967296
```
~~:warning: On 18.04 arc_summary is not installed (https://bugs.launchpad.net/ubuntu/+source/zfs-linux/+bug/1574342)~~
```shell
# Manual download
wget https://raw.githubusercontent.com/zfsonlinux/zfs/master/cmd/arc_summary/arc_summary3
chmod +x arc_summary3
```
Check current in-use values:
```shell
# c      is the target size of the ARC in bytes
# c_max  is the maximum size of the ARC in bytes
# size   is the current size of the ARC in bytes
sudo grep c_max /proc/spl/kstat/zfs/arcstats
sudo grep size /proc/spl/kstat/zfs/arcstats
# In GiB
awk '/^size/ { print $1 " " $3 / 1073741824 }' < /proc/spl/kstat/zfs/arcstats
awk '/^c_max/ { print $1 " " $3 / 1073741824 }' < /proc/spl/kstat/zfs/arcstats
arc_summary | grep zfs_arc_max
arcstat
arcstat 1 10

# Set the c_max at runtime. However the ARC size will not be released automatically
# To force the RAM to be released it is needed to export the zpool
echo $((6*1024*1024*1024)) > /sys/module/zfs/parameters/zfs_arc_max
```
#### Scrub speed
* zfs_resilver_delay: Number of ticks to delay resilver
* zfs_top_maxinflight: Max I/Os per top-level
* https://github.com/zfsonlinux/zfs/wiki/ZFS-on-Linux-Module-Parameters#zfs_resilver_min_time_ms
```
# options zfs zfs_resilver_delay=0
options zfs zfs_resilver_delay=0 zfs_top_maxinflight=64 zfs_resilver_min_time_ms=5000 
# Combine with other options
options zfs zfs_arc_max=4294967296 zfs_resilver_delay=0
```
```shell
# Make sure options are propagated
update-initramfs -u -k all
reboot
# View current options
arc_summary | grep zfs_resilver_delay
arcstat 1 10
```
* http://arstechnica.com/information-technology/2014/02/ars-walkthrough-using-the-zfs-next-gen-filesystem-on-linux/
* https://superuser.com/questions/1137416/how-can-i-determine-the-current-size-of-the-arc-in-zfs-and-how-does-the-arc-rel/1137417#1137417
* https://utcc.utoronto.ca/~cks/space/blog/solaris/ZFSScrubsOurSpeedup
* https://www.matt-j.co.uk/2014/06/25/zfs-on-linux-resilver-scrub-performance-tuning/
* https://superuser.com/questions/1137416/how-can-i-determine-the-current-size-of-the-arc-in-zfs-and-how-does-the-arc-rel/1182488#1182488

* [\[ TOC \]](#table-of-contents)

### Useful ZFS Commands
* http://manpages.ubuntu.com/manpages/bionic/man8/zpool.8.html
* http://manpages.ubuntu.com/manpages/bionic/man8/zfs.8.html

:warning: Use `-nv` options to check what's going to be done
```shell
zpool status
zfs list
zfs create zfs-storage/share
zfs create zfs-storage/compressed

# enable ACL
zfs set acltype=posixacl <dataset>
# turn compression on
# Don't use compression=on, set compression algorithm explicitly
# See also comments to feature@lz4_compress option is zpool creation section
zfs set compression=lz4 zfs-storage/compressed
# check dataset
zpool scrub zfs-storage
# turn on deduplication
zfs set dedup=on zfs-storage/withdedup

# [!] Deletes happen asynchronously, so AVAIL (zfs) and FREE (zpool) take time
# to update after deletion
# Delete dataset (remove -n for actual deletion)
zfs destroy -nv pool/path
# Recursive delete all snapshots. [!!] Dangerous, remove n for actual deletion
zfs destroy -nvr pool/path@%

# Check capacity
zpool list -H -o capacity
# Check compression ratio
zfs get compressratio [dataset]
# View dedup ratio (ZFS deduplication has pool-wide scope and dedup ratio can't be viewed for individual filesystems)
zpool list
# View block statistics (can take long time, use screen)
zdb -b <pool>

# Create snapshot
zfs snapshot pool/path@snapshot
# List snapshots
zfs list -t snapshot
# View snapshots space usage
zfs list -ro space
# Access snapshot content
ls /mountpoint/pool/.zfs/snapshot/snap-name
ls /mountpoint/pool/path/.zfs/snapshot/snap-name

# -H             No header
# -o name        Display snapshot name only
# -s creation    Sort by creation time (use -S for reverse order)
# -d1 pool/path  Recursively display any children of the dataset, limiting
#                the recursion to depth. A depth of 1 will display only the
#                dataset and its direct children.
zfs list -H -t snapshot -o name -s creation -d1 pool/path

# Unmount dataset
zfs unmount pool/path
# Mount dataset
zfs mount pool/path
# View current mounts
zfs mount

# View pools to import
zpool import
# Import pool
# -d dir  Searches for devices or files in dir. The -d option can be specified multiple times.
zpool import -d [/dev/disk/by-id] pool-name
```
* [\[ TOC \]](#table-of-contents)
### Health Monitoring Script

```
cd /root
wget https://github.com/cheretbe/notes/raw/master/linux/files/zfs_health_check.sh
chmod +x zfs_health_check.sh
crontab -e
```
Add daily check and weekly scrub
```
# Check ZFS pool status daily at 8:00
00 08  *  *  *  /root/zfs_health_check.sh
# Scrub ZFS pool every Sunday at 2:00
00 02  *  *  0  /sbin/zpool scrub zfs-data
```
![exclamation](https://github.com/cheretbe/notes/blob/master/images/warning_16.png) ZoL adds its own scrub (check `/etc/cron.d/zfsutils-linux`)

Check if script works:
```shell
# temporarily shift current date for 9 days to trigger
# scrub expiration message (max scrub age is 8 days by default)
service ntp stop
# Ubuntu 16.04
systemctl stop systemd-timesyncd
# CentOS 7
systemctl stop chronyd.service

date --set="$(date) + 9 days"
/root/zfs_health_check.sh

ntpdate -s ru.pool.ntp.org
service ntp start
# Ubuntu 16.04
# systemd-timesyncd changes time gradually, so we change time back manually beforehand
date --set="$(date) - 9 days"
systemctl start systemd-timesyncd
# CentOS 7
systemctl start chronyd.service
```
* Source: https://calomel.org/zfs_health_check_script.html
* Local copy: https://github.com/cheretbe/notes/blob/master/linux/files/zfs_health_check.sh

* [\[ TOC \]](#table-of-contents)

### Move single disk file system to another drive

```shell
# [!] Carefully examine existing pool's (non-default and non-inherited) properties
# and make sure new pool's setup is the same
zpool get feature@lz4_compress pool_name
zfs get -s local,temporary,received -r all pool_name

zfs create ... new_pool ...

zpool get feature@lz4_compress new_pool
zfs get -s local,temporary,received -r all new_pool

zfs snapshot -r pool_name@move

# [!] Note -u flag
# -u   File system that is associated with the received stream is not mounted
zfs send -R pool_name@move | pv | zfs receive -F -u new_pool

# [!] Stop services and disable cron jobs (e.g. sanoid)

zfs snapshot -r pool_name@move-1

zfs send -R -i pool_name@move pool_name@move-1 | pv | zfs receive -F -u new_pool

# Start services and ENABLE cron jobs```
* https://github.com/zfsonlinux/zfs/issues/2121
-----

* [\[ TOC \]](#table-of-contents)

### Replace a Disk in a Pool 
Replacing `/dev/disk/by-id/ata-VBOX_HARDDISK_sn002` -> `/dev/disk/by-id/ata-VBOX_HARDDISK_sn111`
* Planned
```bash
# [!] use screen utility
zpool offline zfs-data /dev/disk/by-id/ata-VBOX_HARDDISK_sn002
# Replace disks
# -f forces use of new device even if it appears to be in use
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
* Notes
    * Pool devices are stored in the binary file `/etc/zfs/zpool.cache`
    * To change `/dev/sdX` device names to `/dev/disk/by-id`: `zpool export pool-name && zpool import -d /dev/disk/by-id pool-name`
* [\[ TOC \]](#table-of-contents)
### Send Over SSH or netcat

* https://forums.freenas.org/index.php?threads/lz4-compression-and-replication.17890/
    * Replication retains the compression
        * uncompressed -> uncompressed: obviously no change
        * compressed -> compressed: compression retains
        * uncompressed -> compressed: destination performs compression
        * compressed -> uncompressed: compression reatains (there can be both compressed and uncompressed blocks in the same filesystem)
    * Deduplication
        * The stream is normally always "non-deduped", even when you are replicating between two deduplicated pools
        * There is a zfs send option (-D) to generate a deduplicated stream (it controls the stream itself, not destination)
        * -D option allows to even send a deduplicated stream between two non-dedup pools
        * non-dedup -> dedup: data is deduplicated on the destination.
        * dedup -> non-dedup: data is NOT deduplicated on the destination (even if with -D option)

:question: Do some tests to find out how ZoL handles compression/deduplication

```shell
# We use -v only on the receiving end since it outputs status only on start and finish.
# Sender with -v option every second outputs status records that look like this:
# 16:13:54   43.9G   pool/path@snapshot

# [!] Check filesystem properties on receiver (e.g. zfs get acltype etc.)

# Receiver (-F option is needed if pool/path exists)
nc -l -p 1234 | pv | zfs receive -v pool/path

# Sender
zfs send -v pool/path@snapshot | nc host.domain.tld 1234

# incremental
zfs snapshot pool/path@new-snapshot
zfs send -v -i pool/path@old-snapshot pool/path@new-snapshot | nc host.domain.tld 1234
zfs destroy pool/path@old-snapshot

# send locally
zfs send pool1/path1@snapshot | zfs receive -F pool2/path2
# with progress
zfs send pool1/path1@snapshot | pv | zfs -v receive -F pool2/path2
# check out results
zfs list -t snapshot -r pool2
# [!!] This will overwrite current data in pool2/path2
zfs rollback pool2/path2@snapshot
# remove snapshots
zfs destroy pool1/path1@snapshot
zfs destroy pool2/path2@snapshot
```
:bulb: Snapshots can be dumped to files (use pigz for compression)
```shell
zfs send pool/path@snapshot > file.img
zfs receive pool/path < file.img
```
Sanoid: https://github.com/cheretbe/notes/blob/master/linux/sanoid.md

* https://unix.stackexchange.com/questions/343675/zfs-on-linux-send-receive-resume-on-poor-bad-ssh-connection
* https://serverfault.com/questions/74411/best-compression-for-zfs-send-recv/408908#408908

* [\[ TOC \]](#table-of-contents)

### Raspberry Pi
* https://github.com/zfsonlinux/zfs/wiki/Building-ZFS
* https://www.raspberrypi.org/forums/viewtopic.php?f=66&t=165247
* (!!!!) https://github.com/zfsonlinux/zfs/wiki/Debian and https://www.raspberrypi.org/forums/viewtopic.php?f=66&t=146108 (try [this](https://raspberrypi.stackexchange.com/questions/12258/where-is-the-archive-key-for-backports-debian-org/12266#12266) to add keys)
Changes:
* Add `/usr/local/lib` to `/etc/ld.so.conf` and run `ldconfig`
* check needed packages (on a clean installation)

```shell
apt install raspberrypi-kernel-headers

echo "deb http://ftp.debian.org/debian jessie-backports main contrib" >> /etc/apt/sources.list.d/backports.list
apt update

# on public key error (e.g. NO_PUBKEY 8B48AD6246925553 NO_PUBKEY 7638D0442B90D010)
gpg --keyserver pgpkeys.mit.edu --recv-key 8B48AD6246925553 7638D0442B90D010
gpg -a --export 8B48AD6246925553 7638D0442B90D010 | sudo apt-key add -

# [!!!] Select <No> in "Abort building ZFS on a 32-bit kernel?" dialog            
apt-get install -t jessie-backports zfs-dkms

dkms status
# Should return output similar to that:
# spl, 0.6.5.9, 4.9.35+, armv7l: installed
# zfs, 0.6.5.9, 4.9.35+, armv7l: installed

# if zfs entry is missing:
dkms --verbose install zfs/0.6.5.9
dkms status
modprobe zfs
```
* [\[ TOC \]](#table-of-contents)

### Unsorted
* https://wiki.archlinux.org/index.php/ZFS
* https://icesquare.com/wordpress/how-to-improve-zfs-performance/
* https://github.com/zfsonlinux/zfs/wiki/Ubuntu-16.04-Root-on-ZFS
* http://www.znapzend.org/
* http://wiki.complete.org/ZFSAutoSnapshots
* https://github.com/leprechau/zfs-replicate
* http://everythingshouldbevirtual.com/zfs-replication-backups
* https://github.com/jimsalterjrs/sanoid

* [\[ TOC \]](#table-of-contents)
