```shell
pvcreate /dev/sdd /dev/sde
vgcreate hdd-sas-2 /dev/sde

# Datacenter > Storage > Add > LVM

pvesm lvmscan
pvesm status
cat /etc/pve/storage.cfg

lvcreate -l 100%FREE -n vm-103-hdd-sas-1 hdd-sas-1
# Force creation when ZFS signatures is found on a drive
# -W|--wipesignatures y|n
lvcreate -Wn -l 100%FREE -n vm-103-hdd-sas-2 hdd-sas-2
# After this newly created lv will appear in "Hardware" tab of VM 103 as "Unused disk 0"
qm rescan
lvrename vg02 lvold lvnew
lvremove /dev/hdd-sas-1/vm-103-hdd-sas-1

cat /etc/pve/storage.cfg
```

## LXC
### Export from LXD (kind of works)
```shell
# On LXD host
lxc publish ssh-tunnels --alias ssh-tunnels-export
# lxc image export [<remote>:]<image> [<target>] [flags]
# The output target is optional and defaults to the working directory
# (but will create a tar.gz file with id as a name)
lxc image export ssh-tunnels-export ssh-tunnels-export
lxc image delete ssh-tunnels-export

# [!] It couldn't be used as is, needs to be repacked
# https://forum.proxmox.com/threads/lxd-to-proxmox.68501/
# PVE container images have flat structure with no extra subdirs and metadata
# LXD images have metadata.yaml and rootfs,templates subdirs
tar xzvf ssh-tunnels-export.tar.gz
cd ssh-tunnels-export
rm -rf rootfs/dev
# This will skip adding rootfs directory in the archive
# https://stackoverflow.com/questions/939982/how-do-i-tar-a-directory-of-files-and-folders-without-including-the-directory-it/39530409#39530409
find rootfs/ -printf "%P\n" | tar -czf ssh-tunnels-repacked.tar.gz --no-recursion -C rootfs -T -

# Copy ssh-tunnels-export.tar.gz to PVE host
scp ssh-tunnels-export.tar.gz root@pm1.domain.tld:/var/lib/vz/template/cache/

# On PVE host
# -password without value will ask for root password
# -rootfs: special syntax STORAGE_ID:SIZE_IN_GiB means allocate a new volume
# https://pve.proxmox.com/pve-docs/pct.1.html
pct create 102 local:vztmpl/ssh-tunnels-export.tar.gz \
  -description "description test" -hostname ssh-tunnels \
  -cores 1 -memory 512 \
  -rootfs volume=ssd-1:10 \
  -nameserver 192.168.1.1 \
  -net0 name=eth0,hwaddr=00:16:3E:9C:02:76,ip=dhcp,bridge=vmbr0 \
  -unprivileged 1 -password
```
