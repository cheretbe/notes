https://samba.ninja/2016/10/ubuntu-16-04-samba-ad-member-server/
https://samba.ninja/2015/10/centos-7-samba-ad-member-server/
https://samba.ninja/2014/10/ubuntu-14-samba-ad-member-server/

### Useful commands
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

### Standalone server
No LDAP, no Windows domain, local users.
Install `samba` package and edit default `/etc/samba/smb.conf`. Run `testparm` after each edit.
``` ini
# Change workgroup and description
workgroup = TEST
server string = %h server (Samba, Ubuntu)

[global]
# follow symlincs settings
follow symlinks = yes
wide links = yes
unix extensions = no
# Disable printing
load printers = no
printing = bsd
printcap name = /dev/null
disable spoolss = yes

# Share with authentication (by default it is tdbsam)
# Password has to be set by: sudo smbpasswd -a <username>
# User needs read or write access to the directory
[test]
  path = /samba/test
  # Groups: @groupname
  read list = npa
  write list = npa
  read only = No
  create mask = 0665
  # For this to work the following GLOBAL param has to be set
  # obey pam restrictions = no
  force create mode = 0665
  force directory mode = 0775
# For DOS file attributes to work with programs like xcopy or robocopy
# user_xattr has to be enabled in /etc/fstab and the following parameters
# turned on
# TODO: check if robocopy actually needs this
  ea support = yes
  store dos attributes = yes
  map system = no
  map archive = no
  map readonly = no

# Anonymous share (set directory owner to nobody:nogroup)
[Anonymous]
comment = Anonymous share
path = /samba/anonymous
writable = yes
guest ok = yes
read only = no
create mask = 0665
directory mask = 0775

# Home directories
[homes]
  comment = Home Directories
  valid users = %S
  read only = No
  create mask = 0700
  directory mask = 0700
```
