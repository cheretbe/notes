* https://insights.ubuntu.com/2016/03/14/the-lxd-2-0-story-prologue
     * Use ZFS
* https://bayton.org/docs/linux/lxd/lxd-zfs-and-bridged-networking-on-ubuntu-16-04-lts/
* https://stgraber.org/2016/10/27/network-management-with-lxd-2-3/#comment-241550

```shell
# apt install -t xenial-backports lxd lxd-client
apt install lxd zfsutils-linux bridge-utils
```

`/etc/network/interfaces`
```
auto br0
iface br0 inet dhcp
	bridge_ports eth0

iface eth0 inet manual
```
Netplan (`/etc/netplan/01-netcfg.yaml`)
```
network:
 version: 2
 renderer: networkd
 ethernets:
   eth0:
     dhcp4: false
 bridges:
   br0:
     interfaces: [eth0]
     dhcp4: false
     addresses: [192.168.1.99/24]
     gateway4: 192.168.1.1
     nameservers:
       addresses: [1.1.1.1,8.8.8.8]
     parameters:
       forward-delay: 0
```
Apply configuration
```
sudo netplan apply
ifconfig
```

```shell
# Manually create loopback file ZFS system
# Create a 30Gb zero-filled file	
dd if=/dev/zero of=/path/to/lxd_zfs.img bs=1024 count=$[1024*1024*30]
# Or create a 30Gb sparse file
dd if=/dev/zero of=/path/to/lxd_zfs.img bs=1 count=0 seek=30G
# Create ZFS pool on it
zpool create -f -o ashift=12 -O atime=off -m none lxd-zfs-loopback /path/to/lxd_zfs.img
```
* https://discuss.linuxcontainers.org/t/reclaim-unused-space-from-var-lib-lxd-zfs-img/338/3

Add to `/etc/sysctl.conf`
```
fs.inotify.max_queued_events = 1048576
fs.inotify.max_user_instances = 1048576
fs.inotify.max_user_watches = 1048576
```
Add to `/etc/security/limits.conf`
```
* soft nofile 100000
* hard nofile 100000
```

Reboot

```shell
sudo usermod --append --groups lxd non_root_user

lxc profile list
lxc profile copy default multibridge
lxc profile edit multibridge
#lxc delete test1 --force
lxc launch ubuntu:xenial test1 -p multibridge
lxc exec test1 bash

lxc config set test1 security.privileged true
lxc config device add test1 dev_ppp unix-char path=/dev/ppp
lxc config edit test1

lxc list
lxc stop container_name
lxc delete container_name

# LXD key                  Correspoding LXC key   Values
# boot.autostart           lxc.start.auto         1 enabled, 0 disabled
# boot.autostart.delay     lxc.start.delay        delay in seconds to wait after starting container
# boot.autostart.priority  lxc.start.order        container priority, higher values means earlier start
lxc config set container_name boot.autostart 0

# Snapshots
# create
lxc snapshot <container>
lxc snapshot <container> <snapshot name>
# list
lxc info <container>
# restore
lxc restore <container> <snapshot name>
# delete
lxc delete <container>/<snapshot name>
# rename
lxc move <container>/<snapshot name> <container>/<new snapshot name>
# creating a new container from a snapshot - identical except for the
# volatile information being reset (MAC address)
lxc copy <source container>/<snapshot name> <destination container>
```
Access files from the host: https://serverfault.com/questions/674762/easy-way-to-transfer-files-between-host-and-lxc-container-on-lvm/676375#676375
:warning: Adjust permissions on host since container's root will not have access
