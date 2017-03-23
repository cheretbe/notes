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

View status
```
apcaccess status
```
