* 2read
    * https://www.delphix.com/blog/delphix-engineering/zfs-raidz-stripe-width-or-how-i-learned-stop-worrying-and-love-raidz
    * http://www.openoid.net/zfs-practicing-failures/
    * https://calomel.org/zfs_raid_speed_capacity.html

### Troubleshooting
* https://openzfs.github.io/openzfs-docs/Basic%20Concepts/Troubleshooting.html
* :warning: 2check https://github.com/maglar0/zpool-events/tree/main
* :bulb: it may be useful to issue `zpool offline` on a dying disk to avoid useless constant resilvering

```shell
# [!] since 2.2.0 corrective "zfs receive" is available.
# Pool needs to be able to overwrite corrupted data. For a single non-redundant drive pool
# this means replacing the drive (see "Move single disk-file system to another drive" section below)
zfs receive -c [-vn] filesystem|snapshot

# -v      Print the entire payload for each event
zpool events -v

# -i internal event information that can be used for diagnostic purposes
# -l long format that includes the user name, the host name, and the zone in which the operation was performed
zpool history pool -i -l

# Cumulative stats for all pools
zpool iostat
# Viev stats for a pool every 2 seconds
zpool iostat pool 2
# View virtuald devices stats
zpool iostat -v
# Continiously watch stats (first page is cumulative data)
watch -n 1 zpool iostat -v 1 2
```

### Disk Identification

```shell
# TODO: move this to partitioning.md
# this shows everything, but truncates model name even with -J (JSON output) option
lsblk --nodeps -e7 -o name,size,model,serial,tran
# this show everything except human-readable size
for device in $(smartctl --scan -j | jq -r '.devices[].name'); do (smartctl -i ${device} -j); done \
  | jq -s -r '.[] | [.device.name,.model_name,.model_family,.serial_number] | @tsv' \
  | column -t -s $'\t'
# This ugly contraption show everything including human-readable sizes %)
# needs a module file present in the current directory
# https://users.aalto.fi/~tontti/posts/jq-and-human-readable-bytes/
for device in $(smartctl --scan -j | jq -r '.devices[].name'); do (smartctl -i ${device} -j); done \
  | jq -s -r 'include "./bytes"; .[] | [.device.name,.model_name,.model_family,.serial_number,(.user_capacity.bytes|bytes)] | @tsv' \
  | column -t -s $'\t'

lsblk --nodeps -e7 -o name,size,serial,wwn,type,tran

# View disk names by id (WWN is preferable if disks support it)
for wwn in $(lsblk --nodeps -e7 -n -o wwn | awk 'NF'); do (ls -lha /dev/disk/by-id | grep -F "${wwn}" | grep -Fv "part"); done
for serial in $(lsblk --nodeps -e7 -n -o serial | awk 'NF'); do (ls -lha /dev/disk/by-id | grep -F "${serial}" | grep -Fv "part"); done

# Prerequisite: jc
# https://github.com/kellyjonbrazil/jc
curl -s https://api.github.com/repos/kellyjonbrazil/jc/releases/latest \
| grep "browser_download_url.*linux-x86_64.tar.gz" \
| cut -d : -f 2,3 \
| tr -d \" \
| wget -i -
# View disks, that are not members of a pool
for serial in $(lsblk --nodeps -e7 -n -o serial | awk 'NF'); do if ! zpool status pool-name | ./jc --zpool-status | jq -r '.[].config[].name' | grep -q "${serial}"; then echo "${serial}"; fi; done
```
#### Add ZFS drive aliases
```shell
# Add aliases
nano /etc/zfs/vdev_id.conf
# alias Lenovo_WMC160231293  wwn-0x50000c0f0129f724
# alias Seagate_Z1X6ZC7G     wwn-0x5000c50085292023
udevadm trigger
ls -lha /dev/disk/by-vdev

# Change drive reference path
zpool export pool
zpool import pool -d /dev/disk/by-vdev
```

### Notifications
* Scripts are in `/etc/zfs/zed.d/`
* Settings are in `/etc/zfs/zed.d/zed.rc` (e.g. ZED_NOTIFY_VERBOSE for resilver_finish-notify.sh)

### Clear ZFS metadata
```shell
# [!!!] Be careful. Double check the host and drive letter
wipefs -a -f /dev/sdX

# Manually
# Clear ZFS metadata at the end(!) of a disk
# https://superuser.com/questions/1248905/how-to-delete-some-zfs-metadata-from-hard-drive
dd if=/dev/zero of=/dev/sda seek=$(($(blockdev --getsz "/dev/sda") - 1024))
```

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

### zpool Creation

* :bulb: See [disk identification](#disk-identification) examples

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
* **-m /mnt/mountpoint** sets mountpoint location instead of /poolname (protect mountpoint: `chattr +i /mnt/mountpoint`)
* **-o feature@lz4_compress=enabled** by default (`-o compression=on`) it's either `lzjb` or `lz4` (if `lz4_compress` feature is enabled)
    * https://github.com/zfsonlinux/zfs/blob/master/man/man8/zfs.8 search for `default compression`
* **-O compression=lz4**
    * Use `lz4` for compressed/mixed/unknown data
    * https://www.servethehome.com/the-case-for-using-zfs-compression/

Change mount point after creation
```shell
zfs set mountpoint=/mountpoint pool/filesystem

# Mount pool recursively
zfs list -rH -o name pool | xargs -L 1 zfs mount
# View what is mounted
findmnt -R pool
```
View current values
```shell
# ashift
# ashift=12: pool is 4K aligned, ashift=9: pool 512B aligned
zdb -C [pool]
# for non-imported pool
zdb -C -e pool

zfs get xattr pool
zfs get atime pool
zfs get mountpoint pool
zfs get compression pool

# lz4_compress
zpool get all [pool] | grep 'feature@lz4_compress'
# or
zpool get feature@lz4_compress [pool]
```

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

### Useful ZFS Commands
* http://manpages.ubuntu.com/manpages/bionic/man8/zpool.8.html
* http://manpages.ubuntu.com/manpages/bionic/man8/zfs.8.html

:warning: Use `-nv` options to check what's going to be done
```shell
# recent versions have version command
# (displays the software version of the zpool userland utility and the ZFS kernel module)
zpool version

zpool status
zfs list
zfs create zfs-storage/share
zfs create zfs-storage/compressed

# enable ACL
zfs set acltype=posixacl <dataset>
# turn compression on
# Don't use compression=on, set compression algorithm explicitly
# See also comments to feature@lz4_compress option is zpool creation section
# [!!] One needs to somehow rewrite existing data in the pool after enabling compression as
# it won't go re-compressing existing blocks
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
# [!!] Use clone (example below)
ls /mountpoint/pool/.zfs/snapshot/snap-name
ls /mountpoint/pool/path/.zfs/snapshot/snap-name

# -H             No header
# -o name        Display snapshot name only
# -s creation    Sort by creation time (use -S for reverse order)
# -d1 pool/path  Recursively display any children of the dataset, limiting
#                the recursion to depth. A depth of 1 will display only the
#                dataset and its direct children.
zfs list -H -t snapshot -o name -s creation -d1 pool/path

zfs clone pool/path@snapshot pool/clone-path
# For clones "ORIGIN" field will contain parent snapshot instead of "-"
zfs list -o name,origin

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


### Move single disk-file system to another drive

* :bulb: See [disk identification](#disk-identification) examples

#### By temporary converting the pool to a mirror

```shell
# Move single-disk pool from /dev/sda to /dev/sdb
# 1. Temporary convert the pool from single-disk to mirror by attaching new disk
#    [!!] /dev/sda is the original drive
#    /dev/sda is necessary: attach [-f] [-o property=value] <pool> <device> <new-device>
zpool attach pool-name /dev/sda /dev/sdb
# 2. Wait for data allocation to complete (will show "resilvering" for sdb)
zpool status
# 3. Detach old disk
zpool detach pool-name /dev/sda
```

#### (old version) Using send
```shell
# [!] Carefully examine existing pool's (non-default and non-inherited) properties
# and make sure new pool's setup is the same
zpool get feature@lz4_compress pool_name
zfs get -s local,temporary,received -r all pool_name

# [!] When copying to a mirrored pool and there are enough physical ports available -
#     do yourself a favor, create mirror right away
zfs create ... new_pool ...

zpool get feature@lz4_compress new_pool
zfs get -s local,temporary,received -r all new_pool

zfs snapshot -r pool_name@move

# [!!!] Be extra careful with mountpoints. At this point new_pool will have the same
#       mountpoint as pool_name. Don't reboot until send/receive is complete.
#       When rebooting later for some reason, be sure to set canmount property
zfs set canmount=noauto new_pool
# [!] Don't forget to reset it to default after reboot
zfs inherit -S canmount new_pool
# [!] Note -u flag
# -u   File system that is associated with the received stream is not mounted
zfs send -R pool_name@move | pv | zfs receive -F -u new_pool
# or use mbuffer without -q
zfs send -R pool_name@move | mbuffer -s 128k -m 300M | zfs receive -F -u new_pool

# [!] Stop services and disable cron jobs (e.g. sanoid)

zfs snapshot -r pool_name@move-1

zfs send -R -i pool_name@move pool_name@move-1 | pv | zfs receive -F -u new_pool

zpool export pool_name
zpool export new_pool
zpool import new_pool pool_name

# Check mountpoint, start services and ENABLE cron jobs
# if for some reason old pool is needed, first import it without mounting, change the mountpoint
# and export/import once again
zpool import pool_name old_pool -N

# Delete snapshots
zfs destroy -nv -r pool_name@move-1
zfs destroy -nv -r pool_name@move
```
* https://github.com/zfsonlinux/zfs/issues/2121
-----


### Replace a Disk in a Pool 

* :bulb: See [disk identification](#disk-identification) examples

Replacing `/dev/disk/by-id/ata-VBOX_HARDDISK_sn002` -> `/dev/disk/by-id/ata-VBOX_HARDDISK_sn111`
* Planned
```bash
# [!!!] use screen utility
zpool offline zfs-data /dev/disk/by-id/ata-VBOX_HARDDISK_sn002
# (?) Disk doesn't go offline when status is FAULTED. Needed to issue 'zpool clear pool id' command
# Anyway, do not proceed until disk status becomes OFFLINE

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
# [!] on secure networks use mbuffer instead
# receiver
mbuffer -4 -s 128k -m 1G -I 1234 | zfs receive -F pool/path
# sender
# [!] -R (--replicate) is not only recursive, but copies all properties, snapshots, descendent
# file systems, and clones. This is not what we usually want by default (mountpoint)
zfs send pool/path@snapshot | mbuffer -s 128k -m 1G -O dest-ip:1234
# https://serverfault.com/a/408908
# What's really interesting is that using mbuffer when sending and receiving on localhost speeds things up as well
# It just goes to show that zfs send/receive doesn't really like latency or any other pauses in the stream to work best
zfs send tank/pool@snapshot | mbuffer -s 128k -m 4G -o - | zfs receive -F tank2/pool

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
# Restore (rollback) snapshot
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

### Unsorted
* https://wiki.archlinux.org/index.php/ZFS
* https://icesquare.com/wordpress/how-to-improve-zfs-performance/
* https://github.com/zfsonlinux/zfs/wiki/Ubuntu-16.04-Root-on-ZFS
* http://www.znapzend.org/
* http://wiki.complete.org/ZFSAutoSnapshots
* https://github.com/leprechau/zfs-replicate
* http://everythingshouldbevirtual.com/zfs-replication-backups
* https://github.com/jimsalterjrs/sanoid
