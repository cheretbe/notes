* https://slackblogs.blogspot.com/2019/02/kernel-44172-breaking-some-application.html
------

Packages to install before guest additions
```
apt install dkms build-essential linux-headers-generic
```

Change default VM location
```shell
vboxmanage setproperty machinefolder /path/to/directory/
# View current setting
vboxmanage list systemproperties | grep "Default machine folder:"

# k, m, g suffix are for Ki, Mi, Gi
sudo mkdir -p /mnt/ramdrive
sudo mount -t tmpfs -o size=16g tmpfs /mnt/ramdrive
vboxmanage setproperty machinefolder /mnt/ramdrive
# change size without losing data
mount -o remount,defaults,noatime,size=32g /mnt/ramdrive/

# fstab entry
# tmpfs  /mnt/ramdrive  tmpfs  defaults,noatime,nodiratime,size=16g  0  0

# Restore default setting
vboxmanage setproperty machinefolder "${HOME}/VirtualBox VMs"
```

To be able to add USB devices on **host** in Linux:
```
sudo adduser <username> vboxusers
```

GUI binary location (Linux): `/usr/bin/virtualbox`
Guest Additions location (Linux): `/usr/share/virtualbox/VBoxGuestAdditions.iso`
View:
```shell
list systemproperties | grep -i 'Default Guest Additions ISO'
```
### Installation

```shell
# Ubuntu 22.04
wget https://www.virtualbox.org/download/oracle_vbox_2016.asc -O /usr/share/keyrings/oracle_vbox_2016.asc
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/oracle_vbox_2016.asc] https://download.virtualbox.org/virtualbox/debian $(lsb_release -cs) contrib" > /etc/apt/sources.list.d/virtualbox.list
apt update
apt install virtualbox-6.1
apt install virtualbox-7.0
apt install virtualbox-7.1
```

### Emulating failed disk drive

* https://www.redhat.com/en/blog/linux-block-devices-hints-debugging-and-new-developments
* https://blogs.oracle.com/linux/post/error-injection-using-dm-dust
* https://www.kernel.org/doc/html/latest/admin-guide/device-mapper/dm-dust.html

```shell
# Apparently all the following is also applicable to a physical machine

device_name=/dev/sdc
# Doesn't survive a reboot (will have to research if the need arises)
# on error view dmesg for details
echo "0 $(blockdev --getsize $device_name) linear $device_name 0" | dmsetup create bad_disk

# [!] Don't forget to unmount or do zfs export
dmsetup suspend bad_disk
# There is also a flakey target - a combo of linear and error that sometimes succeeds.
# Also a delay to introduce intentional delays for testing.
# And dust, see comments below
# on error view dmesg for details
echo -e "0 20000 linear $device_name 0\n20000 500 error\n20500 $(($(blockdev --getsize $device_name) - 20500)) linear $device_name 20500" | dmsetup reload bad_disk
dmsetup resume bad_disk

dmsetup remove bad_disk
```

### Sample vboxmanage commands
```shell
# Move a VM to a new location
vboxmanage movevm <uuid|vmname> --type basic --folder /mnt/data/vm/__vagrant

# List all VMs
vboxmanage list vms
# List running VMs
vboxmanage list runningvms

# Resize a disk
# 15Gb – 15360
# 20Gb – 20480
# 25Gb – 25600
# 30Gb – 30720
# 50Gb - 51200
# in bytes: --resizebyte
VBoxManage modifyhd <path to vdi> --resize <new size in megabytes>
# VBoxManage won't resize VMDK files. The workaround is to clone to VDI
# and then resize
# https://stackoverflow.com/questions/11659005/how-to-resize-a-virtualbox-vmdk-file/12456219#12456219

# Run a command on guest
vboxmanage guestcontrol testvm-2del run --wait-stdout --wait-stderr --username vagrant --password $AO_DEFAULT_VAGRANT_PASSWORD  -- "%comspec%" /c powershell \$psversiontable
# Create a directory on guest
vboxmanage guestcontrol testvm-2del mkdir --username vagrant --password $AO_DEFAULT_VAGRANT_PASSWORD --parents c:\\temp
# Copy files(s) to guest
# [!] Note forward slash for --target-directory even on Windows guests
vboxmanage guestcontrol testvm-2del copyto --username vagrant --password $AO_DEFAULT_VAGRANT_PASSWORD --target-directory c:/temp file1.txt file2.txt
```

### Fix multipath daemon error about missing path

Syslog entry example:
```
multipathd[1766]: sdb: failed to get udev uid: Invalid argument
```
```shell
# Identify virtual disks
sudo lshw -class disk

# Blacklist virtual disks
cat <<EOF | sudo tee -a /etc/multipath.conf
blacklist {
  device {
    vendor "VBOX"
    product "HARDDISK"
  }
}
EOF

# Verify settings
cat /etc/multipath.conf

# Restart multipath daemon
sudo systemctl restart multipathd.service

# Inspect blacklist
sudo multipathd show blacklist
```

### Disable time sync
```shell
VBoxManage setextradata <NAME> "VBoxInternal/Devices/VMMDev/0/Config/GetHostTimeDisabled" 1
VBoxManage setextradata <NAME> "VBoxInternal/TM/TSCTiedToExecution" 1

# For some time tests it's easier to temporarily shift time like this (1 day = 86400000 ms)
VBoxManage.exe modifyvm <NAME> --biossystemtimeoffset <OFFSET in ms>
```


### Using a Physical Hard Drive with a VirtualBox VM

Linux
```bash
# Make sure that current user is a member of groups "vboxusers" and "disk"
groups | grep -e vboxusers -e disk
# If not, add, log off and log on again
sudo usermod -a -G vboxusers <username>
sudo usermod -a -G disk <username>
# Create virtual hard drive
VBoxManage internalcommands createrawvmdk -filename /path/to/file.vmdk -rawdisk /dev/sda
```

### Shared Folders Write Access in Linux
Access to auto-mounted shared folders is only granted to the user group vboxsf, which is created by the VirtualBox Guest Additions installer. Hence guest users have to be member of that group to have read/write access or to have read-only access in case the folder is not mapped writable.
```shell
sudo adduser <username> vboxsf
# or
usermod -a -G vboxsf <username>

# manually mount a shared folder in guest
sudo mount -t vboxsf <sharename> /mont/point
# set the default file owner user and group
sudo mount -t vboxsf <sharename> /mount/point -o uid=vagrant,gid=vagrant
```
`/etc/fstab` entry example:
```
share_name  /path/to/mountpoint  vboxsf  rw,exec,uid=vagrant,gid=vboxsf,dmode=775,fmode=664  0   0
```
### Compacting VDI
#### Linux
The most simple way is to boot from Live CD (to avoid remounting `/` as readonly)
```shell
# Install zerofree (enable universe)
add-apt-repository "deb http://archive.ubuntu.com/ubuntu $(lsb_release -sc) universe"
apt-get update
apt-get install zerofree
# Clear root
zerofree –v /dev/sda1
# Clear the swap space, assuming it is /dev/sda5
swapoff /dev/sda5
blkid /dev/sda5 -s UUID -o value > uuid.tmp
dd if=/dev/zero of=/dev/sda5 bs=1M
mkswap /dev/sda5
swaplabel -U $(cat uuid.tmp) /dev/sda5
```
In the host
```
 VBoxManage modifyhd --compact <disk_name>.vdi
```


### Create dynamic VDI
```
VBoxManage createhd --filename <path to your vdi> --size <size in megabytes>
```
* 15Gb – 15360
* 20Gb – 20480
* 25Gb – 25600
* 30Gb – 30720

### Virtual disks identification
```shell
# IDE
VBoxManage setextradata "VMName" "VBoxInternal/Devices/piix3ide/0/Config/PrimaryMaster/SerialNumber" "091118FC1221NCJ6G8GG"
VBoxManage setextradata "VMName" "VBoxInternal/Devices/piix3ide/0/Config/PrimaryMaster/FirmwareRevision" "FC2ZF50B"
VBoxManage setextradata "VMName" "VBoxInternal/Devices/piix3ide/0/Config/PrimaryMaster/ModelNumber" "HITACHI HTD723216L9SA60"
# SATA
VBoxManage setextradata "VMname" "VBoxInternal/Devices/ahci/0/Config/Port0/SerialNumber" "serial"
VBoxManage setextradata "VMname" "VBoxInternal/Devices/ahci/0/Config/Port0/FirmwareRevision" "firmware"
VBoxManage setextradata "VMname" "VBoxInternal/Devices/ahci/0/Config/Port0/ModelNumber" "model"
```
In the client
```shell
# Linux
lshw -class disk
```

