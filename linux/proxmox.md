* port **8006**

:warning::warning: `/etc/pve` folder is a virtual file system that is provided by the pve-cluster service.
Its content is in `/var/lib/pve-cluster/config.db` SQLite file
```shell
sqlite3 /var/lib/pve-cluster/config.db 'select * from tree' | less
```
* https://forum.proxmox.com/threads/how-to-mount-etc-pve-in-rescue-mode.12496/

## Installation

* :warning: Since DHCP is not an option (see below), when changing static ip after editing `/etc/networking/interfaces` don't forget to update `/etc/hosts` entry
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
* Apt sources
  ```shell
  sed -i 's/^deb https/#&/' /etc/apt/sources.list.d/pve-enterprise.list
  sed -i 's/^deb https/#&/' /etc/apt/sources.list.d/ceph.list
  echo "deb http://download.proxmox.com/debian/pve bookworm pve-no-subscription" > /etc/apt/sources.list.d/pve-no-subscription.list
  ```
* SSL certificate for Web UI
  ```shell
  # /etc/pve/local is a node specific symlink to /etc/pve/nodes/NODENAME
  cp host.domain.tld.crt /etc/pve/local/pve-ssl.pem
  cp host.domain.tld.key /etc/pve/local/pve-ssl.key
  systemctl restart pveproxy.service
  ```
* Add new user
  * Counter-intuitive as usual
    * First add user in `Datacenter` > `Persmissions` > `Users`
    * Then select `Datacenter` > `Permissions` and click `Add` > `User Permission` **there**
    * `Permissions` button in `Datacenter` > `Persmissions` > `Users` shows read-only combination of effectiver permissions
    * https://forum.proxmox.com/threads/add-new-administrator-user.102650/
    * :warning: Some actions are available as root only (at the minimum install updates, attach USB devices)
  * API tokens are in `Datacenter` > `Persmissions` > `API tokens`
* DHCP
  * Using dhcp and 127.0.1.1 in `/etc/host` leads to error: `[main] crit: Unable to resolve node name 'node-name' to a non-loopback IP address - missing entry in '/etc/hosts' or DNS?`
  * There is an (ugly) hack
    * https://weblog.lkiesow.de/20220223-proxmox-test-machine-self-servic/proxmox-server-dhcp.html
    * create /etc/dhcp/dhclient-exit-hooks.d/update-etc-hosts file with the following content
    ```bash
    if ([ $reason = "BOUND" ] || [ $reason = "RENEW" ])
    then
      sed -i "s/^.*\sproxmox.home.lkiesow.io\s.*$/${new_ip_address} proxmox.home.lkiesow.io proxmox/" /etc/hosts
    fi
  * looks fragile as developers might add some additional check or automatic modification of /etc/network/interfaces any time
* Renaming a node
  * TL;DR: Not feasible
  * [Everything breaks down] https://forum.proxmox.com/threads/proxmox-node-name-change.14327/
    * One needs to analyse a lot of files and change god knows how many entries
* Clusters
  * Very strict limitations
    * Nodes can be added/removed only if there are no VMs/containers on it
    * Renaming a node becomes effectively impossible - same problems as with a single node plus cluster config files (:warning: replicated on each node of a cluster)

## API

```shell
# Note '!' usage together with "$var"
# There is no easy way to escape an ! in double quotes, so this is a reasonable workaround
# https://superuser.com/questions/133780/in-bash-how-do-i-escape-an-exclamation-mark
# Authorization header has a form of PVEAPIToken=USER@REALM!TOKENID=UUID

# Get available space
curl -H "Authorization: PVEAPIToken=ansible@pve"'!'"ansible_pve_token=$my_token" https://pm1.domain.tld:8006/api2/json/nodes/pm1/storage/local/status | jq '.data.avail'

# Download an image
# 1. Start download task (node and storage parameters are mandatory)
#    content="import" supports only .ova images (make sure storage has "Import" option in "Content" property)
task_id=$(curl --fail-with-body -sS -H "Authorization: PVEAPIToken=ansible@pve"'!'"ansible_pve_token=$my_token" \
  --data-urlencode content="iso" \
  --data-urlencode url="https://cloud-images.ubuntu.com/noble/current/noble-server-cloudimg-amd64.img" \
  --data-urlencode filename="noble-server-cloudimg-amd64.img" \
  --data-urlencode node="pm1" \
  --data-urlencode storage="local" \
  -X POST \
   https://pm1.domain.tld:8006/api2/json/nodes/pm1/storage/local/download-url |
     jq -r '.data'
)
# 2. Check status (running|stopped)
#    In UI it is in Datacenter > Nodes > mp1 > Task History (current tasks are below under "Logs")
task_status=$(curl --fail-with-body -sS -H "Authorization: PVEAPIToken=ansible@pve"'!'"ansible_pve_token=$my_token" \
  https://pm1.domain.tld:8006/api2/json/nodes/pm1/tasks/${task_id}/status |
    jq -r '.data.status'
)
# 3. Check result when stopped (should be "OK")
task_result=$(curl --fail-with-body -sS -H "Authorization: PVEAPIToken=ansible@pve"'!'"ansible_pve_token=$my_token" \
  https://pm1.domain.tld:8006/api2/json/nodes/pm1/tasks/${task_id}/status |
    jq -r '.data.exitstatus'
)
```

#### VM creation gotchas
As always everything is not quite straightforward 🙂 There is no easy way to use existing qcow2 image using API only. Situation summary as of 28.04.2005
* [download-url](https://pve.proxmox.com/pve-docs/api-viewer/index.html#/nodes/{node}/storage/{storage}/download-url) method doesn't support downloading VM images, only `iso` (`.iso`, `.img`), `import` (`.ova`), vztmpl (?)
    * https://bugzilla.proxmox.com/show_bug.cgi?id=4141
* There is no way to copy QCOW2 image saved as an `.img` to a datastore using API. There is a workaround: use `import-from` parameter during VM creation. But it doesn't support copying from "images" section of a store ("local:images/debian-12-generic-amd64.img" fails). So a dirty hack is needed to use a workaround: place image file under non-existent VM ID (as suggested [here](https://www.reddit.com/r/Proxmox/comments/y51x5h/qemu_importfrom_qcow2_without_root/))
* This leaves 3 options to create a VM
    * 1. Download `.ova` archive using `content="import"` option, create a template from it and then use Ansible `community.general.proxmox_kvm` module to create a VM from this template
        * pros: can be done using API only, template is easy to use for manual VM creation
        * cons: uses additional storage space, template needs changing parameters after creation (controller types etc.)
    * 2. Download `.qcow2` image as `.img` using `content="iso"` option, create a diskless template, use console command `qm importdisk <vm_id> /var/lib/vz/template/iso/noble-server-cloudimg-amd64.img <storage_name>` to create a disk and attach this disk to template
          * pros: reusable template
          * cons: console command usage as root, rather difficult logic to figure out VM ID and local file path
    * 3. Download `.qcow2` image file directly to a non-existing VM ID local directory `/var/lib/vz/images/999/`, then create a VM using `import-from=local:images/debian-12-generic-amd64.img` parameter
          * pros: uses less disk space
          * cons: ugly hack, manual VM creation will require `qm importdisk` usage

## LVM

Disk identification
```shell
# Disk names in the UI (scsi0, etc)
#   Hard Disk (scsi0)
#   Hard Disk (scsi1)
# Will have corresponding serials in the VM:
lsblk --nodeps -o NAME,SERIAL
# NAME SERIAL
# sda  drive-scsi0
# sdb  drive-scsi1
```

```shell
pvcreate /dev/sdd /dev/sde
vgcreate hdd-sas-2 /dev/sde

# Datacenter > Storage > Add > LVM
# [!!] Select Datacenter object iself, then click storage item in the right
#      panel (not Storage subitem in the tree on the left)

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
Remove an LVM disk
```shell
# 1. Make sure the disk in not used in the VM (zpool detach, umount + /etc/fstab edit etc.)
# 2. Detach disk from the VM
# 3. Detached disk will change its status to "Unused Disk x". Select it and click "Delete". This will delete the LV
# 4. Remove VG and PV if there are no LVs left
#    Datacenter > Storage > Remove
#    [!!] Select Datacenter object iself, then click storage item in the right
#      panel (not Storage subitem in the tree on the left)
vgscan
pvscan
vgremove hdd-sas-X
pvscan
pvremove /dev/sdX
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
