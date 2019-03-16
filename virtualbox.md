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
```

To be able to add USB devices on **host** in Linux:
```
sudo adduser <username> vboxusers
```

GUI location (Linux): `/usr/bin/virtualbox`
Guest Additions location (Linux): `/usr/share/virtualbox/VBoxGuestAdditions.iso`
View:
```shell
list systemproperties | grep -i 'Default Guest Additions ISO'
```

### Sample vboxmanage commands
```shell
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

# Run a command on guest
vboxmanage guestcontrol testvm-2del run --wait-stdout --wait-stderr --username vagrant --password $AO_DEFAULT_VAGRANT_PASSWORD  -- "%comspec%" /c powershell \$psversiontable
# Create a directory on guest
vboxmanage guestcontrol testvm-2del mkdir --username vagrant --password $AO_DEFAULT_VAGRANT_PASSWORD --parents c:\\temp
# Copy files(s) to guest
# [!] Note forward slash for --target-directory even on Windows guests
vboxmanage guestcontrol testvm-2del copyto --username vagrant --password $AO_DEFAULT_VAGRANT_PASSWORD --target-directory c:/temp file1.txt file2.txt
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
sudo mount -t vboxsf <sharename> /mont/point -o uid=vagrant,gid=vagrant
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

