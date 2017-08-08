* https://wiki.archlinux.org/index.php/ZFS
* https://icesquare.com/wordpress/how-to-improve-zfs-performance/
* https://github.com/zfsonlinux/zfs/wiki/Ubuntu-16.04-Root-on-ZFS
* http://www.znapzend.org/
* http://wiki.complete.org/ZFSAutoSnapshots
* https://github.com/leprechau/zfs-replicate
* http://everythingshouldbevirtual.com/zfs-replication-backups

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

### 2. Memory tuning
`/etc/modprobe.d/zfs.conf` – may be needed in Linux, since ZFS ARC (Advanced Replacement Cache) can release memory with a delay. If the machine is a dedicated file server, this setting may not be needed
```
# value is in bytes!
# 16GB=17179869184, 8GB=8589934592, 4GB=4294967296, 2GB=2147483648, 1GB=1073741824
options zfs zfs_arc_max=4294967296
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
```
* http://arstechnica.com/information-technology/2014/02/ars-walkthrough-using-the-zfs-next-gen-filesystem-on-linux/
* https://superuser.com/questions/1137416/how-can-i-determine-the-current-size-of-the-arc-in-zfs-and-how-does-the-arc-rel/1137417#1137417

### 3. Create zpool
```
zpool create -f -o ashift=12 -O atime=off zfs-storage raidz1 /dev/disk/by-id/ata-ST1000NM0011_Z1N1VTW3 …
```
* **-o ashift=12** uses 4K blocks instead of 512K (this increases performance especially on large disks)
* **-O atime=off** Disables access time updates
* **-f** option forces creation on errors (like existing data on disk etc.)
* **-m /mnt/mountpoint** sets mountpoint location instead of /poolname
Change mount point after creation
```
zfs set mountpoint=/mountpoint pool/filesystem
```
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

# Check compression ratio
zfs get compressratio [dataset]
# View dedup ratio (ZFS deduplication has pool-wide scope and dedup ratio can't be viewed for individual filesystems)
zpool list
# View block statistics
zdb -b <pool>

# Create snapshot
zfs snapshot pool/path@snapshot
# List snapshots
zfs list -t snapshot
# View snapshots space usage
zfs list -ro space
# Access snapshot content
ls /mountpoint/pool/.zfs/snapshot/snap-name
```
### 5. Set up health monitoring script

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

Check if script works:
```shell
# temporarily shift current date for 9 days to trigger
# scrub expiration message (max scrub age is 8 days by default)
service ntp stop
# Ubuntu 16.04
systemctl stop systemd-timesyncd
date --set="$(date) + 9 days"
/root/zfs_health_check.sh
ntpdate -s ru.pool.ntp.org
service ntp start
# Ubuntu 16.04
# systemd-timesyncd changes time gradually, so we change time back manually beforehand
date --set="$(date) - 9 days"
systemctl start systemd-timesyncd
```
Source :https://calomel.org/zfs_health_check_script.html

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
### 7. Send over SSH or netcat

```shell
# server
nc -l -p 1234 | zfs receive -v pool/path

# client
zfs send -v pool/path@snapshot | nc host.domain.tld 1234

# incremental
zfs snapshot pool/path@new-snapshot
zfs send -v -i pool/path@old-snapshot pool/path@new-snapshot | nc host.domain.tld 1234
zfs destroy pool/path@old-snapshot
```

* https://unix.stackexchange.com/questions/343675/zfs-on-linux-send-receive-resume-on-poor-bad-ssh-connection
* https://serverfault.com/questions/74411/best-compression-for-zfs-send-recv/408908#408908

### 8. Rasberry Pi
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
