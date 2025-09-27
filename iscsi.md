* https://linux.die.net/man/5/targets.conf
* https://www.howtoforge.com/tutorial/how-to-setup-iscsi-storage-server-on-ubuntu-2004-lts/
* https://www.brandonhan.net/posts/configure-iscsi-initiator-and-mount-via-fstab/
* https://www.thegeekdiary.com/iscsi-connection-command-examples-cheat-sheet/

### Server (target) config
```shell
apt install tgt
```

`/etc/tgt/conf.d/iscsi.conf` example:
```
<target iqn.2020-07.example.com:lun1>
     backing-store /dev/mapper/iscsi_temp-disk_lv
     initiator-address 192.168.10.0/24
     incominguser test example_pwd
</target>
```

```shell
systemctl restart tgt
tgtadm --mode target --op show
```

### Client (initiator) config

```shell
apt install open-iscsi
# Generated initiator name
cat /etc/iscsi/initiatorname.iscsi

iscsiadm -m discovery -t sendtargets -p 192.168.10.105
# will output something like
# 192.168.10.105:3260,1 iqn.2020-07.example.com:lun1
# and generate a corresponding config
# [!!] re-running discovery will overwrite existing configs
nano /etc/iscsi/nodes/iqn.2020-07.example.com\:lun1/192.168.10.105\,3260\,1/default
# Add user and password settings
# node.session.auth.username = test
# node.session.auth.password = example_pwd
# to connect on startup
# node.startup = automatic

# list node records
# will output something like
# 192.168.10.105:3260,1 iqn.2020-07.example.com:lun1
# |                     |
# +-- -p --portal       +-- -T --targename
iscsiadm --mode node

# connect manually
iscsiadm -m node --login -p 192.168.10.105:3260,1 --targetname iqn.2020-07.example.com:lun1
# disconnect
iscsiadm -m node --logout -p 192.168.10.105:3260,1 --targetname iqn.2020-07.example.com:lun1

# view the current iSCSI connection (login) status
iscsiadm -m session
# Detailed info
# -P 3 sets the "print" (or "output") level to 3, which shows detailed information about each iSCSI session.
iscsiadm -m session -P 3
```
