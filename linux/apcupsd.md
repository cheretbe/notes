
On a desktop system UPower daemon contros the UPS.
```shell
# Settings are in /etc/UPower/UPower.conf
systemctl status upower

# Enumerate devices
upower -e
# View status
upower -i /org/freedesktop/UPower/devices/ups_hiddev0
```
Use `Power Statistics` (`gnome-power-statistics`) to view status and stats.


Config is in `/etc/apcupsd/apcupsd.conf`:
```
# COM
UPSCABLE smart
UPSTYPE apcsmart
DEVICE /dev/ttyS0

# USB 
UPSCABLE usb
UPSTYPE usb
DEVICE

BATTERYLEVEL 15
MINUTES 5

# Network master/slave link
# Set NETSERVER parameter to on in master's config file
# On slave:
UPSCABLE ether 
UPSTYPE net
#DEVICE <ip>:<port>
DEVICE 192.168.0.101:3551
```

In `/etc/default/apcupsd` change ISCONFIGURED parameter
```
ISCONFIGURED=yes
```

```bash
# View status
apcaccess status
# View/change parameters, run tests (apcupsd service must be stopped)
sudo apctest
```

Custom shudown script. Create `/etc/apcupsd/doshutdown` file and make sure it is executable.
```bash
#!/bin/bash
WALL=wall

# This script is triggered in case of a power failure

echo "Running custom shutdown script..." | ${WALL}
# Custom commands

echo "Finished custom shutdown script..." | ${WALL}

# Exit code 99 - apccontrol stops after this script, no shutdown of this host. For testing purposes.
# Exit code 0  - apccontrol continues with shutdown after this script.
exit 99
```
##### Note
(from apcupsd manual). You can change the apccontrol behavior for every single action. To customize, create a file with the same name as the action, which is passed as a command line argument. Put your script in the `/etc/apcupsd` directory.


When testing the real power fail shutdown (pulling the power plug) it is convinient to temporarily set TIMEOUT parameter to 30. Doing so will cause apcupsd to attempt to shutdown the system 30 seconds after it detects a power failure. :warning: **Don't forget to change it back after tests.** Also always wait for your UPS to **power itself off**, or power if off manually before restarting your computer. Power off grace period can be quite long.

```shell
# Monitor important parameters during tests
watch -n 5 "apcaccess status | grep -E 'BCHARGE|MBATTCHG|MINTIMEL|TIMELEFT|TONBATT'"
```

Ubuntu 16.04 bug: https://bugs.launchpad.net/ubuntu/+source/apcupsd/+bug/1634572

### Network UPS Tools

* https://networkupstools.org/

`apctest` didn't show commands for changing device name and batterydate for APC 750 with "COM" cable. NUT was able to do this, however.

```shell
# [!] This uninstalls apcupsd package and masks apcupsd.service
apt install nut nut-client
nano /etc/nut/ups.conf
```

```
[apc]
    driver = apcsmart
    port = /dev/ttyS0
```
```shell
nano /etc/nut/nut.conf
```
```
MODE=standalone
```
```shell
nano /etc/nut/upsd.users
```
```
[admin]
  password = p@ssw0rd
  actions = SET
  instcmds = ALL
```

```shell
systemctl restart nut-server
upsc apc
upsrw -s "ups.id=APC 750" apc
upsrw -s "battery.date=12/28/23"
upsc apc

# list commmands
upscmd -l apc

upscmd apc calibrate.start
```
