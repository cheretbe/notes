* https://github.com/zfsonlinux/pkg-zfs/wiki/HOWTO-use-a-zvol-as-a-swap-device
* https://www.digitalocean.com/community/tutorials/how-to-add-swap-space-on-ubuntu-16-04
* http://askubuntu.com/questions/33697/how-do-i-add-a-swap-partition-after-system-installation/33703#33703

```shell
# Identify configured swap devices and files
cat /proc/swaps
# Memory usage in human-readable format
free -h

# Disable swap device
swapoff /dev/sda5

# Turn off all swap devices
swapoff -a

# Create a swap file as large as the computer's RAM
# conv=CONVS  convert the file as per the comma separated symbol list
#             notrunc: do not truncate the output file
dd if=/dev/zero of=/swapfile bs=$(cat /proc/meminfo | awk '/MemTotal/ {print $2}') count=1024 conv=notrunc

mkswap /swapfile
# insecure permissions 0644, 0600 suggested.
chmod 600 /swapfile
swapon /swapfile

# /etc/fstab entry
# /swapfile  none  swap  sw  0  0
```
#### Limiting swap for containers

```shell
# Check if configured correctly
# Should *not* return "WARNING: No swap limit support"
docker info
```
(not needed for Ubuntu 22.04?) In order to enable swap accounting the boot argument `swapaccount=1` must be set. This can be done by appending it to the `GRUB_CMDLINE_LINUX_DEFAULT` variable in `/etc/default/grub`, then running `update-grub` as root and rebooting (:warning: check `/etc/default/grub.d/` contents).
```shell
# View current kernel configuraion
# Should return "CONFIG_MEMCG_SWAP=y" 
cat /boot/config-$(uname -r) | grep CONFIG_MEMCG_SWAP
# View current kernel boot parameters
cat /proc/cmdline
```


#### Hibernation

[hibernation.md](./hibernation.md)

#### Find out processes that use max swap

`htop` [doesn't show swap](https://hisham.hm/htop/index.php?page=faq) column. Yes, it's not 100% accurate, but most of the time it doesn't matter: I just need to quickly see what eats my swap. Approximate numbers are fine, just don't show this column by default (and possibly warn user if they turn this column on). Anyway, thankfully `top` does exactly that (without a warning part).

in `top` turn on swap display and sort by this column:
<kbd>f</kbd>, move cursor to `SWAP`, press <kbd>space</kbd>, then <kbd>s</kbd>, <kbd>q</kbd> to close fields management.

Then use `htop` to view process tree (to find a process by PID just start typing digits).

#### Swappines
Add to `/etc/sysctl.conf`:
```
vm.swappiness = 1
```
```shell
# Apply changes without a reboot
sysctl vm.swappiness=1
# Check current setting
cat /proc/sys/vm/swappiness
```
