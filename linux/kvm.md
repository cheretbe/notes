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
* Run Ubuntu 20.04+ on low-memory VPS
    * https://www.downtowndougbrown.com/2021/06/how-to-run-ubuntu-20-04-server-with-only-256-mb-of-ram/
    * https://unix.stackexchange.com/questions/270390/how-to-reduce-the-size-of-the-initrd-when-compiling-your-kernel#comment1280075_270416
    * https://www.hillenius.net/post/nospaceleft/
```shell
ls /boot -lha
cp /etc/initramfs-tools/initramfs.conf{,.bak}
# MODULES=most => MODULES=dep
# COMPRESS=zstd => COMPRESS=xz
nano /etc/initramfs-tools/initramfs.conf

update-initramfs -u
# initrd.img-5.15.0-56-generic has shrunk from 103M to 29M
ls /boot -lha
```


* High utilization when Windows 10 guest is idle: https://www.reddit.com/r/VFIO/comments/80p1q7/high_kvmqemu_cpu_utilization_when_windows_10/
  * Worked for `machine='pc-i440fx-bionic'` on Ubuntu 18.04 (try using default values when moving to a 22.04 host)
```xml
  <!-- before: this config uses over 15% of a host CPU core -->
  <clock offset='localtime'>
    <timer name='rtc' tickpolicy='catchup'/>
    <timer name='pit' tickpolicy='delay'/>
    <timer name='hpet' present='no'/>
    <timer name='hypervclock' present='yes'/>
  </clock>

  <!-- after: this config drops to about 3% of a host CPU core -->
  <clock offset='localtime'>
    <timer name='hpet' present='yes'/>
    <timer name='hypervclock' present='yes'/>
  </clock>
```

* :warning: A hack for KVM cloud provders (Digital Ocean etc)
    * :bulb: Consider using [sdelete](https://learn.microsoft.com/en-us/sysinternals/downloads/sdelete) beforehand
```shell
# source
python3 -m http.server
# destination
wget -O- http://192.168.0.1:8000/windows10.img | dd of=/dev/vda


# destination
netcat -l -p 1234 | dd of=/dev/sda
# source
# use fdisk -l to find out the size
dd if=/dev/sdb | pv -s 21474836480 | netcat 192.168.0.1 1234

# destination
# -d force decompression
nc -l 1234 | bzip2 -d | dd bs=16M of=/dev/sdX

# source
# -c  output to stdout
dd bs=16M if=/dev/sdX | pv | bzip2 -c | nc 192.168.0.1 1234
# [!] Make sure image.img is preallocated raw, not qcow2
pv image.img | bzip2 -c | nc 192.168.0.1 1234

# destination
# Doesn't seem to have any difference with netcat on a 100Mbit channel
mbuffer -q -4 -s 16M -m 1G -I 1234 | bzip2 -d | dd bs=16M of=/dev/sdX

# source
# use fdisk -l to find out the size
dd bs=16M if=/dev/sdX | pv -s 21474836480 | bzip2 -c | mbuffer -q -s 16M -m 1G -O host.domain.tld:1234
```

* :warning: https://www.downtowndougbrown.com/2021/06/how-to-run-ubuntu-20-04-server-with-only-256-mb-of-ram/
* :warning: A temporary workaround for keyboard not working on Ubuntu 22.04 (`virt-viewer` shows `Unknown keycode mapping '(unnamed)'` errov message): use vnc display instead of spice (https://bugzilla.redhat.com/show_bug.cgi?id=1534324)
* `2read`: https://www.reddit.com/r/zfs/comments/514k2r/kvm_zfs_best_practices/d79fdzi/
* `2read`: https://jrs-s.net/2013/05/17/kvm-io-benchmarking/
* Ubuntu. Package to enter password for remote connections over SHH: `ssh-askpass`
* https://sebastian.marsching.com/wiki/Linux/KVM
* Shutdown script on Ubuntu 16.04: `/usr/lib/libvirt/libvirt-guests.sh` (uses settings from `/etc/default/libvirt-guests`)
* CPU host passthrough: `<cpu mode='host-passthrough'/>`

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
usermod -a -G kvm,libvirt username
# https://bugs.launchpad.net/ubuntu/+source/virt-manager/+bug/1550983
# If virt-manager fails to start with error message "Couldn't open libGL.so.1: libGL.so.1:
# cannot open shared object file: No such file or directory"
apt install libgl1-mesa-glx
```
* http://wiki.stoney-cloud.org/wiki/Workaround_unhandled_rdmsr/wrmsr
* Swappiness: https://github.com/cheretbe/notes/blob/master/linux/swap.md#swappines
* Adjust `SHUTDOWN_TIMEOUT` in `/etc/default/libvirt-guests` as needed

### Services

```shell
# Services (Ubuntu 18.04)
# libvirt-bin.service is an alias to libvirtd.service
systemctl list-units libvirt-guests.service libvirtd.service qemu-kvm.service
# UNIT                   LOAD   ACTIVE SUB     DESCRIPTION                                  
# libvirt-guests.service loaded active exited  Suspend/Resume Running libvirt Guests        
# libvirtd.service       loaded active running Virtualization daemon                        
# qemu-kvm.service       loaded active exited  QEMU KVM preparation - module, ksm, hugepages

systemctl list-unit-files libvirt-guests.service libvirtd.service qemu-kvm.service
# UNIT FILE              STATE   
# libvirt-guests.service disabled
# libvirtd.service       disabled
# qemu-kvm.service       enabled

# Stop all guests
systemctl stop libvirt-guests

# Start all guests
systemctl restart libvirtd
```

### Networking

* https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/virtualization_deployment_and_administration_guide/sect-managing_guest_virtual_machines_with_virsh-managing_virtual_networks

#### Bridged

```shell
sudo netplan generate
# [!!] Reverting custom parameters for bridges and bonds is not supported
#      try shows a message: "Please carefully review the configuration and use 'netplan apply' directly.
sudo netplan apply
```

Netplan config example
```yaml
network:
  version: 2
  ethernets:
    enp4s0:
      optional: true
      dhcp4: false
  bridges:
    enp4s0-br:
      optional: true
      interfaces: [enp4s0]
      dhcp4: true
      parameters:
        forward-delay: 0
```

:warning: Very detailed explanation: https://linuxconfig.org/how-to-use-bridged-networking-with-libvirt-and-kvm

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
```shell
# [!!!] bridge info
brctl show
brctl showmacs enp2s0-br
# List bridges
ip link show type bridge
# List interfaces which are part of a bridge
ip -c link show master enp2s0-br
```
* http://manpages.ubuntu.com/manpages/xenial/man5/bridge-utils-interfaces.5.html
* http://manpages.ubuntu.com/manpages/xenial/en/man8/brctl.8.html

#### Isolated

* https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/configuring_and_managing_virtualization/configuring-virtual-machine-network-connections_configuring-and-managing-virtualization#virtual-networking-isolated-mode_types-of-virtual-machine-network-connections


Method 1 - just click "+" in "Virtual Networks" tab and enter parameters

Method 2 - Manual (use `virsh net-edit network_name` if virt-manager doesn't support editing XML)

```bash
# Generate randomized MAC address
printf 'DE:AD:BE:EF:%02X:%02X\n' $((RANDOM%256)) $((RANDOM%256))
# Generate UUID (uuid-runtime package)
uuidgen
```

```xml
<network>
  <name>intnet1</name>
  <uuid>00000000-0000-0000-0000-000000000000</uuid>
  <bridge name="virbr1" stp="on" delay="0"/>
  <mac address="00:00:00:00:00:00"/>
  <domain name="intnet1"/>
  <ip address="192.168.144.1" netmask="255.255.255.0">
  </ip>
</network>
```

```bash
virsh net-list --all
virsh net-dumpxml default

virsh net-define intnet1.xml
virsh net-start intnet1
virsh net-autostart intnet1
```

[\[ TOC \]](#table-of-contents)

### Local storage pool

```shell
virsh pool-define-as --name hdd1 --type dir --target /mnt/hdd1/vm
virsh pool-start hdd1
virsh pool-autostart hdd1
# Sounds dangerous, but only stops the pool
virsh pool-destroy hdd1
# [!] This is dangerous as it deletes underlying directory /mnt/hdd1/vm
virsh pool-delete hdd1
virsh pool-undefine hdd1
```

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
# Use -o preallocation=off|meta|full|falloc option (falloc)
# Specify -f raw for raw disks
# [!] Use screen if connected via SSH
qemu-img resize -f raw --preallocation=falloc /var/lib/libvirt/images/test-0.img +5G
qemu-img resize /var/lib/libvirt/images/test-0.img +10G

# Convert qcow2 to VDI
qemu-img convert -f qcow2 image.qcow2 -O vdi image.vdi
```

[\[ TOC \]](#table-of-contents)
