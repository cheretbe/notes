```bash
# Use full capacity of multiple drives with different sizes (metadata mirrored, data not mirrored and not striped)
mkfs.btrfs -d single /dev/sdb /dev/sdc
# Once you create a multi-device filesystem, you can use any device in the FS for the mount command
mount /dev/sdc /mnt
# View filesystems
btrfs filesystem show
```

* https://btrfs.wiki.kernel.org/index.php/FAQ
* https://btrfs.wiki.kernel.org/index.php/Using_Btrfs_with_Multiple_Devices
