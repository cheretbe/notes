```bash
# Use full capacity of multiple drives with different sizes (metadata mirrored, data not mirrored and not striped)
mkfs.btrfs -d single /dev/sdb /dev/sdc
# Once you create a multi-device filesystem, you can use any device in the FS for the mount command
# for /etc/fstab use UUID (btrfs filesystem show to view)
mount /dev/sdc /mountpoint

# View filesystems
btrfs filesystem show
# For image files (e.g. LXD storage) view current mounts to find the image file itself
mount | grep btrfs
findmnt -t btrfs

# Run balance (this is not a backround operation, use screen)
time btrfs balance start /mountpoint
# View balance status
btrfs balance status /mountpoint
# Cancel balance
btrfs balance cancel /mountpoint

# Add device
btrfs device add /dev/sdc /mountpoint
# Delete device
btrfs device delete /dev/sdc /mountpoint
# Delete missing device (disk is completely dead and has already been removed)
btrfs device delete missing [/mountpoint]

# Reclame (some) unused space for image file
fstrim -v /var/lib/lxd/storage-pools/default
```

* https://btrfs.wiki.kernel.org/index.php/FAQ
* https://btrfs.wiki.kernel.org/index.php/Using_Btrfs_with_Multiple_Devices
