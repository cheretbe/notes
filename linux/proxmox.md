* port **8006**

:warning::warning: `/etc/pve` folder is a virtual file system that is provided by the pve-cluster service.
Its content is in `/var/lib/pve-cluster/config.db` SQLite file
```shell
sqlite3 /var/lib/pve-cluster/config.db 'select * from tree' | less
```
* https://forum.proxmox.com/threads/how-to-mount-etc-pve-in-rescue-mode.12496/

## Installation

* Stuck on detecting video card
  * Navigate to Install Proxmox VE (Terminal UI) and press <kbd>e</kbd> to edit the entry. Using the arrow keys, navigate to the line starting with linux, move the cursor to the end of that line and add the parameter nomodeset, separated by a space from the pre-existing last parameter.
  * https://pve.proxmox.com/pve-docs/chapter-pve-installation.html#nomodeset_kernel_param
* Stuck on "Trying to detect country"
  * Still happening on a fresh install on version 8.1. Got past it by going to a shell (Alt+F3 for me) then killing the traceroute process (`kill -9 <pid>`).
* Remove "You do not have a valid subscription for this server" message
  * https://dannyda.com/2020/05/17/how-to-remove-you-do-not-have-a-valid-subscription-for-this-server-from-proxmox-virtual-environment-6-1-2-proxmox-ve-6-1-2-pve-6-1-2/
    ```shell 
    cp /usr/share/javascript/proxmox-widget-toolkit/proxmoxlib.js{,.bak}
    sed -i.backup -z "s/res === null || res === undefined || \!res || res\n\t\t\t.data.status.toLowerCase() \!== 'active'/false/g" /usr/share/javascript/proxmox-widget-toolkit/proxmoxlib.js
    systemctl restart pveproxy.service
  ```
  * press Ctrl+F5 or Shift+F5 to reload page ignoring cache

## LVM

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
### Images
* http://download.proxmox.com/images/system/
* https://forum.proxmox.com/threads/lxc-containers-from-images-linuxcontainers-org-images.55383/
* https://forum.proxmox.com/threads/import-lxc-container-template-from-linuxcontainers-org.141090/
* download of 'http://download.proxmox.com/images/system/ubuntu-22.04-standard_22.04-1_amd64.tar.zst' to '/var/lib/vz/template/cache/ubuntu-22.04-standard_22.04-1_amd64.tar.zst' finished

```shell
# LXD images (not usable, see export from LXD)
# https://images.linuxcontainers.org/streams/v1/images.json
# https://images.linuxcontainers.org/images/
lxc image list --format yaml ubuntu:
```


### Export from LXD (kind of works, see comment at the end)
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

# [!!!] But all this doesn't work properly
# - unprivileged container doesn't start (at least no output in the console)
# - privileged container starts ok, but pct changes many things on creation (the most
#   notable thing is host SSH keys). See 'Guest Operating System Configuration' section
#   in https://pve.proxmox.com/pve-docs/pct.1.html
#   Also there are lots of errors in system log (need to compare with source container, it's
#   quite probable that those errors are due to LXC limitations)
#  - "--ostype unmanaged" setting skips container config mentioned above. But it leads to even
#    more errors in system log (and SSH doesn't start at all). So the config might be necessary after all

# [!] Possible way to fix all this is to use backups by creating backup metadata in the orginal tar.gz archive
# Looks like metadata are stored in pct.conf and  pct.fw files in /etc/vzdump
# Notes (container name) are in /var/lib/vz/dump/vzdump-lxc-102-2024_04_14-22_44_49.tar.gz.notes
# But setting all this to correct values doesnt work. "Show Configuration" in the UI shows error
# Will need to analyze backup structure more thogouhly (if I ever get round to all this at all)
pct restore 102 local:backup/vzdump-lxc-102-2024_04_14-22_44_49.tar.gz -ignore-unpack-errors 1 -unprivileged
```
