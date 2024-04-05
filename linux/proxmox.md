```shell
pvcreate /dev/sdd /dev/sde
vgcreate hdd-sas-2 /dev/sde

# Datacenter > Storage > Add > LVM

pvesm lvmscan
pvesm status
cat /etc/pve/storage.cfg

lvcreate -l 100%FREE -n vm-103-hdd-sas-1 hdd-sas-1
# Force creation when ZFS signatures is found on a drive
# -W|--wipesignatures y|n
lvcreate -Wn -l 100%FREE -n vm-103-hdd-sas-2 hdd-sas-2
# After this newly created lv will appear in "Hardware" tab of VM 103 as "Unused disk 0"
qm rescan
lvrename vg02 lvold lvnew
lvremove /dev/hdd-sas-1/vm-103-hdd-sas-1

cat /etc/pve/storage.cfg
```
