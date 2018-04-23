* https://insights.ubuntu.com/2016/03/14/the-lxd-2-0-story-prologue
     * Use ZFS
* https://bayton.org/docs/linux/lxd/lxd-zfs-and-bridged-networking-on-ubuntu-16-04-lts/

```shell
apt install lxd zfsutils-linux bridge-utils
```

`/etc/network/interfaces`
```
auto br0
iface br0 inet dhcp
	bridge_ports eth0

iface eth0 inet manual
```

```shell
# Manually create loopback file ZFS system
# Create a 30Gb zero-filled file	
dd if=/dev/zero of=/path/to/lxd_zfs.img bs=1024 count=$[1024*1024*30]
# Or create a 30Gb sparse file
dd if=/dev/zero of=/path/to/lxd_zfs.img bs=1 count=0 seek=30G
# Create ZFS pool on it
zpool create -f -o ashift=12 -O atime=off -m none lxd-zfs-loop /path/to/lxd_zfs.img
```
* https://discuss.linuxcontainers.org/t/reclaim-unused-space-from-var-lib-lxd-zfs-img/338/3
