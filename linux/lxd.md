* **https://lxd.readthedocs.io/en/latest/**
* https://insights.ubuntu.com/2016/03/14/the-lxd-2-0-story-prologue
     * Use ZFS
* https://bayton.org/docs/linux/lxd/lxd-zfs-and-bridged-networking-on-ubuntu-16-04-lts/
* https://stgraber.org/2016/03/11/lxd-2-0-blog-post-series-012/
* https://stgraber.org/2016/10/27/network-management-with-lxd-2-3/#comment-241550
* https://github.com/lxc/lxd/blob/master/doc/cloud-init.md

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
sudo netplan generate
sudo netplan apply
# View debug info
sudo netplan --debug apply
networkctl list
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

# Default loopback pool:
# Pool name: default
# Image file: /var/lib/lxd/disks/default.img

# Temporarily import an offline pool without mounting it
# Use file's parent directory (not full file path)
zpool import -d /path/to/image/dir -N pool-name
zpool export pool-name
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

sudo lxd init

# https://lxd.readthedocs.io/en/latest/storage/
# Use the existing ZFS Zpool "pool"
lxc storage create pool1 zfs source=pool
# Use the existing ZFS dataset "pool/path"
lxc storage create pool1 zfs source=pool/path

# Growing a loop-backed ZFS pool
# https://github.com/lxc/lxd/blob/master/doc/storage.md#growing-a-loop-backed-zfs-pool

# Moving a loop-backed pool file to another location: see below

lxc network list
lxc network edit lxdbr0 

lxc profile list
lxc profile copy default multibridge
lxc profile edit multibridge
#lxc delete test1 --force
# List images available from LXD image store, including unofficial ones ([!] note trailing colon)
lxc image list images:
# List ubuntu images only
lxc image list ubuntu:

lxc launch ubuntu:xenial test1
lxc launch ubuntu:bionic test2

lxc image list images: "centos"
lxc image list images: "centos/6/amd64"
lxc launch images:centos/7/amd64 test

lxc launch ubuntu:xenial test1 -p multibridge
# Create a container without launching it
lxc init ubuntu:xenial test1 -p multibridge
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
lxc config set container_name boot.autostart 1

# Copy a container without enabling remote access
lxc stop test1
lxc publish test1 --alias test1-export
lxc image export test1-export test1-export
lxc image delete test1-export
# Copy test1-export.tar.gz file manually
lxc image import test1-export --alias test1-imported
lxc init test1-imported test1 [-p custom-profile]
lxc image delete test1-imported

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
Config is in `/var/lib/lxd/lxd.db`
```shell
sqlite3 /var/lib/lxd/lxd.db '.tables'
sqlite3 /var/lib/lxd/lxd.db '.schema containers_config'
sqlite3 /var/lib/lxd/lxd.db 'SELECT * FROM containers_config'
sqlite3 /var/lib/lxd/lxd.db 'SELECT cont.name,conf.key,conf.value FROM containers_config AS conf INNER JOIN containers AS cont on conf.container_id = cont.id WHERE cont.name = "container-name"'
```

**Port forwarding**
```shell
# 1. Add a proxy device on container mycontainer, giving it an arbitrary name (myport80)
# 2. Set it up to listen on all (0.0.0.0) network interfaces on the host, port 80. Could be changed to something more specific
# 3. Set it up to make connections to the container mycontainer on the localhost interface at port 80
lxc config device add mycontainer myport80 proxy listen=tcp:0.0.0.0:80 connect=tcp:localhost:80
lxc config device add mycontainer myport443 proxy listen=tcp:0.0.0.0:443 connect=tcp:localhost:443
```
* https://discuss.linuxcontainers.org/t/forward-port-80-and-443-from-wan-to-container/2042/2
* https://lxd.readthedocs.io/en/latest/containers/#type-proxy

**Mounting local directory in a container**

```shell
# 1. Expand the range of uid and gid available by editing /etc/subuid and /etc/subgid
cp /etc/subuid{,.bak}
cp /etc/subgid{,.bak}

cat /etc/subuid
lxd:100000:1000000000
root:100000:1000000000
...

cat /etc/subgid
lxd:100000:1000000000
root:100000:1000000000
...

cat /etc/login.defs | grep -v "#" |  grep -v "^$"

# 2. Restart lxd to apply changes
shell
sudo systemctl restart lxd

# 3. Enable isolated idmap for a container
lxc config set container-name security.idmap.isolated true
lxc restart container-name

# 4. Allow LXD’s use of user uid and gid
printf "lxd:$(id -u username):1\nroot:$(id -u username):1\n" | sudo tee -a /etc/subuid
printf "lxd:$(id -g username):1\nroot:$(id -g username):1\n" | sudo tee -a /etc/subgid
```

* https://ubuntu.com/blog/custom-user-mappings-in-lxd-containers
* https://dacrib.net/rant/2018/06/07/how-to-mount-a-local-directory-or-volume-with-lxd/
* https://discuss.linuxcontainers.org/t/looking-for-clarification-about-subuid-gid/630

Access files from the host: https://serverfault.com/questions/674762/easy-way-to-transfer-files-between-host-and-lxc-container-on-lvm/676375#676375<br>
`/var/lib/lxd/storage-pools/default/containers/`<br>
:warning: Adjust permissions on host since container's root will not have access<br>
Less hackerish approach:
```
lxc exec container2 -- mv /home/user/file.txt{,.bak}
lxc file pull container1/home/user/file.txt file.txt
lxc file push file.txt container2/home/user/file.txt --mode 644 --uid 1003 --gid 1003
```

* https://discuss.linuxcontainers.org/t/how-to-set-public-ips-for-each-container-in-lxd-3-0-0-ubuntu-18-04/1712/7
* https://blog.simos.info/how-to-preconfigure-lxd-containers-with-cloud-init/
* https://packetpushers.net/cloud-init-demystified/
* https://cloudinit.readthedocs.io/en/latest/topics/network-config-format-v1.html
* https://github.com/lxc/lxd/blob/master/doc/cloud-init.md


Network config

Static address (2check):
```shell
lxc exec container /bin/bash
echo 'network: {config: disabled}' > /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg
vim /etc/netplan/50-cloud-init.yaml
netplan apply # or just reboot to be sure.
```
* https://finalx.nl/en/articles/ubuntu-rdp

Doesn't work?:
```shell
lxc launch ubuntu:18.04 test --config=user.network-config="$(cat network-config.yaml)"

# Edit later (how to apply?)
lxc config set test user.network-config - < network-config.yaml
```
`network-config.yaml`:
```yaml
version: 1
config:
    - type: physical
      name: eth0
      subnets:
          - type: static
            ipv4: true
            address: 192.168.1.29/24
            gateway: 192.168.1.1
            control: auto
#    - type: nameserver
#      address:
#        - 1.1.1.1
#        - 1.0.0.1
#      search:
#        - domain.tld
```
Config locations in container
```shell
/etc/cloud/cloud.cfg
/var/lib/cloud/seed/nocloud-net/network-config
# 18.04
/etc/netplan/50-cloud-init.yaml
# 16.04
/etc/network/interfaces.d/50-cloud-init.cfg 
```

Moving loop-backed ZFS pool file:
```shell
# This most likely will fail with 'pool is busy' message
# -f option doesn't work on Linux:
# https://github.com/zfsonlinux/zfs/issues/2435
# [!!!] Note the pool name, we will need it on import
zpool export lxd-default

# Stopping LXD services doesn't help
# We need to temporarily disable them and reboot
systemctl disable lxd-containers.service lxd.socket
reboot
zpool export lxd-default

# Move file to a new location and import it back
# Use file's parent directory (not full file path)
zpool import -d /new/path/ -N lxd-default

systemctl enable lxd-containers.service lxd.socket
systemctl is-enabled lxd-containers.service lxd.socket
systemctl start lxd
```
