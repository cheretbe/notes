## Table of Contents
* [Unsorted](#unsorted)
* [Guest Settings](#guest-settings)
* [Installation](#installation)
* [Networking](#networking)
* [LVM Storage Pool](#lvm-storage-pool)
* [VLAN](#vlan)
* [Copying \(editing\) a VM](#copying-editing-a-vm)
* [virsh Commands](#virsh-commands)

### Unsorted
* Ubuntu. Package to enter password for remote connections over SHH: `ssh-askpass`
* https://sebastian.marsching.com/wiki/Linux/KVM
* Shutdown script on Ubuntu 16.04: `/usr/lib/libvirt/libvirt-guests.sh` (uses settings from `/etc/default/libvirt-guests`)

[\[ TOC \]](#table-of-contents)

### Guest Settings
Windows Virtio drivers: https://fedoraproject.org/wiki/Windows_Virtio_Drivers#Direct_download

Enable policy: Local Computer Policy > Computer Configuration > Windows Settings > Security Settings > Local Policies > Security Options `"Shutdown: Allow system to be shut down without having to log on"` 
```batch
:: Query current policy setting
reg.exe QUERY "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v shutdownwithoutlogon
:: If it is 0x0, update to 0x1
reg.exe ADD "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v shutdownwithoutlogon /t REG_DWORD /d 0x1 /f
:: Update policies
gpupdate /force
```

Shutdown timeout
```batch
:: Query current ShutdownWarningDialogTimeout value
reg.exe QUERY "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows" /v ShutdownWarningDialogTimeout
:: If it is 0xffffffff, update to 0x00000001
reg.exe ADD "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows" /v ShutdownWarningDialogTimeout /t REG_DWORD /d 0x1 /f
```

Power option "Turn off the display" has to be set to off

Force XP shutdown even if there are logged in users (![exclamation](https://github.com/cheretbe/notes/blob/master/images/warning_16.png) This setting forces MessageBox function to automatically choose the default button)
```batch
:: Query current policy setting
reg.exe QUERY "HKLM\SYSTEM\CurrentControlSet\Control\Error Message Instrument" /v EnableDefaultReply
:: If it is 0x0 or not present, update to 0x1
reg.exe ADD "HKLM\SYSTEM\CurrentControlSet\Control\Error Message Instrument" /v EnableDefaultReply /t REG_DWORD /d 0x1 /f
```
* http://mindref.blogspot.ru/2011/04/kvm-shutdown-windows-guest-gracefullly.html
* https://pve.proxmox.com/wiki/Windows_2012_guest_best_practices

```shell
# SHUTDOWN_TIMEOUT is in /etc/default/libvirt-guests
# Check last shutdown status
journalctl -b -1 -u 'libvirt-guests'
```
Failed shutdown log example
```
Feb 17 17:40:29 ubuntu-test libvirt-guests.sh[1726]: Timeout expired while shutting down domains
Feb 17 17:40:29 ubuntu-test systemd[1]: libvirt-guests.service: Control process exited, code=exited status=1
Feb 17 17:40:29 ubuntu-test systemd[1]: libvirt-guests.service: Failed with result 'exit-code'.
Feb 17 17:40:29 ubuntu-test systemd[1]: Stopped Suspend/Resume Running libvirt Guests.
```

[\[ TOC \]](#table-of-contents)

### Installation
To check if hardware acceleration is enabled install package `cpu-checker` and run `kvm-ok` as root. KVM is basically a hardware-accelerated version of QEMU
``` bash
apt update
apt install bridge-utils qemu-kvm virt-manager
# Add a user to kvm and libvirtd groups (logoff/logon to take effect)
usermod -a -G kvm,libvirtd username
# https://bugs.launchpad.net/ubuntu/+source/virt-manager/+bug/1550983
# If virt-manager fails to start with error message "Couldn't open libGL.so.1: libGL.so.1:
# cannot open shared object file: No such file or directory"
apt install libgl1-mesa-glx
```
* http://wiki.stoney-cloud.org/wiki/Workaround_unhandled_rdmsr/wrmsr
* Swappiness: https://github.com/cheretbe/notes/blob/master/linux/swap.md#swappines
* Adjust `SHUTDOWN_TIMEOUT` in `/etc/default/libvirt-guests` as needed
### Networking
Add bridged network adapter to `/etc/network/interfaces`
```
auto eth0
iface eth0 inet manual

auto br0
iface br0 inet static
  address 192.168.1.2
  netmask 255.255.255.0
  #network 192.168.1.0
  #broadcast 192.168.1.255
  gateway 192.168.1.1
  dns-nameservers 192.168.1.1
  dns-search home.local
  # [!!!] Make sure bridge-utils package is installed
  bridge_ports eth0
  bridge_fd 0
  bridge_hello 2
  brigge_maxage 12
  #bridge_stp off
```
Some info on bridge parameters:
* http://manpages.ubuntu.com/manpages/xenial/man5/bridge-utils-interfaces.5.html
* http://manpages.ubuntu.com/manpages/xenial/en/man8/brctl.8.html

[\[ TOC \]](#table-of-contents)

### LVM storage pool

In `virt-manager` click "Add new storage pool", select Type "logical: LVM Volume Group".
Use the "Target Path" field to **either** select an existing LVM volume group or as the name for a new volume group. The default format is `storage_pool_name/lvm_Volume_Group_name`.

Examples
1. Existing VG
    - Target Path: /dev/vm_name_backup_vg
    - Sorce Path: leave empty
    - Build Pool: unchecked
2. Create VG
    - Target Path: /dev/vm_name_backup_vg
    - Sorce Path: /dev/sda1
    - Build Pool: checked

* https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/7/html/Virtualization_Deployment_and_Administration_Guide/sect-LVM_based_storage_pools.html

[\[ TOC \]](#table-of-contents)

## VLAN
```bash
apt install vlan
# Load kernel module
modprobe 8021q
# Add VLAN with id 100 to eth0
vconfig add eth0 100
# Assign an address to the new interface
ip addr add 10.0.0.1/24 dev eth0.100

# Make this setup permanent
echo "8021q" >> /etc/modules
# /etc/network/interfaces
# auto eth0.100
# iface eth0.100 inet dhcp
#   vlan-raw-device eth0
```

[\[ TOC \]](#table-of-contents)

### Copying (editing) a VM
Copy the VM's disks from `/var/lib/libvirt/images` on src host to the same dir on destination host
```shell
# on the source host run
virsh dumpxml VMNAME > domxml.xml
# and copy this xml to the dest. host
# on the destination host run
virsh define domxml.xml
```
Start new VM.
If the disk location differs, you need to edit the xml's devices/disk node to point to the image on the destination host. If the VM is attached to custom defined networks, you'll need to either edit them out of the xml on the destination host or redefine them as well
```shell
virsh net-dumpxml > netxml.xml
# and
virsh net-define netxml.xml && virsh net-start NETNAME & virsh net-autostart NETNAME
```
To edit existing (registered) vm:
```shell
export EDITOR=nano
virsh edit vmname
```
VM's configs are in `/etc/libvirt/qemu`
* http://serverfault.com/questions/434064/correct-way-to-move-kvm-vm

[\[ TOC \]](#table-of-contents)

### virsh Commands

```shell
# Enable/disable/list autostarting VMs
virsh autostart <vmname>
virsh autostart <vmname> --disable
virsh list --autostart --all

qemu-img create -f qcow2 /mnt/backup/backup-rescue.qcow2 3449633080320
# [!] Check -o preallocation=off|meta|full|falloc option (falloc)
# Specify -f raw for raw disks
qemu-img resize /var/lib/libvirt/images/test-0.img +10G
```

[\[ TOC \]](#table-of-contents)
