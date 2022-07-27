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
