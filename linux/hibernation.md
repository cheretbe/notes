```shell
swapoff /swapfile

# Create swap file at least as large as the computer's RAM
dd if=/dev/zero of=/swapfile bs=$(cat /proc/meminfo | awk '/MemTotal/ {print $2}') count=1024 conv=notrunc

mkswap /swapfile
swapon /swapfile

blkid $(df -P / | tail -1 | cut -d' ' -f 1)

filefrag -v /swapfile

# Filesystem type is: ef53
# File size of /swapfile is 16419532800 (4008675 blocks of 4096 bytes)
#  ext:     logical_offset:        physical_offset: length:   expected: flags:
#    0:        0..   63487:      34816..     98303:  63488:
#                                |<------ we need this

nano /etc/default/grub
# Update GRUB_CMDLINE_LINUX_DEFAULT value
# GRUB_CMDLINE_LINUX_DEFAULT="quiet splash resume=UUID=xxx resume_offset=yyy"

update-grub

```
