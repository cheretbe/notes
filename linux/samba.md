https://samba.ninja/2016/10/ubuntu-16-04-samba-ad-member-server/
https://samba.ninja/2015/10/centos-7-samba-ad-member-server/
https://samba.ninja/2014/10/ubuntu-14-samba-ad-member-server/

###Useful commands
``` shell
# Everything as root
# View stats
smbstatus
# Show locks only
smbstatus -L
# For a specific user
smbstatus -u <username>
# Sessions and shares only
net status sessions
net status shares
# List current samba group map to local groups
net groupmap list
# Change password
smbpasswd –a <username>
# Test smb.conf
testparm
testparm -s
# View tdbsam user list (-v: verbose)
sudo pdbedit -L -v
```
