Config is in `/etc/apcupsd/apcupsd.conf`:
```
# USB 
UPSCABLE usb
UPSTYPE usb
DEVICE

# Network link
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

When testing the real power fail shutdown (pulling the power plug) is convinient to temporarily set TIMEOUT parameter to 30. Doing so will cause apcupsd to attempt to shutdown the system 30 seconds after it detects a power failure. Don't forget to change it back after tests.

