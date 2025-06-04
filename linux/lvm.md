
> Even if LVM itself doesn't care about having a real partition, one reason to create it anyway
> is to inform partitioning programs that there's "something there."
> A nightmare scenario is a new sysadmin diagnosing a boot problem on a server,
> firing up a partitioning program, seeing unpartitioned disks, and concluding that the drive is corrupt.
* https://serverfault.com/questions/439022/does-lvm-need-a-partition-table/439026#439026

```shell
pvs
vgs
lvs
```

parted
```
mklabel gpt
mkpart primary 1M 100%
set 1 lvm on
```

creation
```shell
apt install lvm2

pvcreate /dev/sdb1 [/dev/sdc1]
pvdisplay

vgcreate vg_name /dev/sdb1 [/dev/sdc1]
vgdisplay

# Size[UNIT]
# Size is an input number that accepts an optional unit.  Input units are always treated as base two values, regardless
# of capitalization, e.g. 'k' and 'K' both refer to 1024.  The default input  unit  is  specified by letter, followed by |UNIT.
# UNIT represents other possible input units: b|B is bytes, s|S is sectors of 512 bytes, k|K is KiB, m|M is MiB, g|G is GiB,
# t|T is TiB, p|P is PiB, e|E is EiB.  (This should not be confused with the output control --units, where capital letters mean
# multiple of 1000.)
# hint: use b for bytes
lvcreate --name lv_name --size 100G name_vg
# All free space
lvcreate --name lv_name -l +100%FREE name_vg

lvdisplay
```

### Resize without a reboot
```shell
# 60G -> 100G
df -h
# /dev/mapper/system--vg-rootfs   59G   38G   20G  67% /
lsblk
# sda                     8:0    0   60G  0 disk 
# `-sda1                  8:1    0   60G  0 part 
#   `-system--vg-rootfs 252:0    0   60G  0 lvm  /

# Change disk size on the hypervisor
# Rescan
echo '1' > /sys/class/scsi_disk/1\:0\:0\:0/device/rescan
# On 'No such file or directory' error just use Tab completion after scsi_disk part

lsblk
# sda                     8:0    0  100G  0 disk 
# `-sda1                  8:1    0   60G  0 part 
#   `-system--vg-rootfs 252:0    0   60G  0 lvm  /

fdisk -l /dev/sda
# Make sure partition type is 8e
# Device     Boot Start       End   Sectors Size Id Type
# /dev/sda1  *     2048 125781250 125779203  60G 8e Linux LVM

fdisk /dev/sda
# 1. d (delete)
# 2. n (new) -> p (primary) -> 1 -> default -> default
# 3. t (type) -> 8e
# 4. p - check if everything is ok
# 5. w

lsblk
partprobe -s
lsblk
# sda                     8:0    0  100G  0 disk 
# `-sda1                  8:1    0  100G  0 part 
#   `-system--vg-rootfs 252:0    0   60G  0 lvm  /

pvscan
# PV /dev/sda1   VG system-vg       lvm2 [59.97 GiB / 0    free]
pvresize /dev/sda1
pvscan
# PV /dev/sda1   VG system-vg       lvm2 [100.00 GiB / 40.02 GiB free]

lvscan
# ACTIVE            '/dev/system-vg/rootfs' [59.97 GiB] inherit
lvresize -l+100%FREE /dev/system-vg/rootfs
lvscan
# ACTIVE            '/dev/system-vg/rootfs' [100.00 GiB] inherit

df -h
# /dev/mapper/system--vg-rootfs   59G   38G   20G  67% /
resize2fs /dev/system-vg/rootfs
df -h
# /dev/mapper/system--vg-rootfs   99G   38G   57G  40% /
```
