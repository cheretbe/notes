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
# Manually create loop filesystem
# Create a 30Gb zero-filled file
dd if=/dev/zero of=/path/to/zfs_image bs=1024 count=$[1024*1024*30]
# View first unused device
losetup -f
# Create the device
losetup /dev/loop0 /path/to/zfs_image
# List loop devices
losetup -a
# [??] How to make it permanent?
```
