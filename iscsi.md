### Server config

### Client config

```shell
iscsiadm -m discovery -t sendtargets -p 192.168.10.105
# will output something like
# 192.168.10.105:3260,1 iqn.2020-07.example.com:lun1
# and generate a corresponding config
# [!!] re-running discovery will overwrite existing configs
nano /etc/iscsi/nodes/iqn.2020-07.example.com\:lun1/192.168.10.105\,3260\,1/default
# to connect on startup
# node.startup = automatic

# connect manually
iscsiadm -m node --login -p 192.168.10.105:3260,1 --targetname iqn.2020-07.example.com:lun1
# disconnect
iscsiadm -m node --logout -p 192.168.10.105:3260,1 --targetname iqn.2020-07.example.com:lun1
```
