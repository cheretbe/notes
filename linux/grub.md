* Options in `GRUB_CMDLINE_LINUX` are always effective.
* Options in `GRUB_CMDLINE_LINUX_DEFAULT` are effective ONLY during normal boot (NOT during recovery mode).


```
GRUB_DEFAULT='Windows 8 (loader) (on /dev/sda1)'
```

### Reset password

* https://www.tecmint.com/reset-forgotten-root-password-in-debian/
  * press <kbd>e</kbd> in grub to enter edit mode
  * locate the line that begins with `linux`, just after `ro quiet` append `init=/bin/bash`
  * press <kbd>Ctrl</kbd>+<kbd>x</kbd> or <kbd>F10</kbd> to boot
  * remount root fs to rw: `mount -n -o remount,rw /`
  * change password with `passwd [user]`
  * unmount root fs just in case `umount /`
  * reboot (note the -f option) `reboot -f`

### Repair
Boot from LiveCD
```shell
sudo -i
# Mount root partition
mount /dev/sdXX /mnt
# Only if there is a separate boot partition
mount /dev/sdYY /mnt/boot

mount --bind /dev /mnt/dev
mount --bind /dev/pts  /mnt/dev/pts
mount --bind /proc /mnt/proc
mount --bind /sys /mnt/sys
mount --bind /usr/ /mnt/usr

# Chroot and repair
chroot /mnt
update-grub
grub-install /dev/sdX
# Check installation
grub-install --recheck /dev/sdX

# Exit chroot: CTRL-D on the keyboard
umount /mnt/usr
umount /mnt/dev/pts
umount /mnt/dev
umount /mnt/proc
umount /mnt/sys

#(if was mounted)
umount /mnt/boot

sudo umount /mnt
```
