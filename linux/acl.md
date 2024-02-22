### Installation
```shell
apt install acl
# check for acl option
tune2fs -l /dev/sda1 | grep "Default mount options"
zfs get acltype [dataset]
```
### Masks
1. `umask` is the file mode creation mask (it is also a function that sets the mask). Subtracting the mask value from the default permissions gives us the actual permissions. In other words, if a permission is set in the umask value it will not be set in the permissions applied to the directory or file. The umask values work as an inverse of the usual permission values.
* 0: No permissions are removed
* 1: The execute bit is unset in the permissions
* 2: The write bit is unset in the permissions
* 4: The read bit is unset in the permissions

```shell
# Default value is set by UMASK setting in /etc/login.defs (typically 022 these days)
grep UMASK /etc/login.defs
# This completely removes "other" permissions for current shell
umask 004
# Use subshell to temporarily set umask for one command only
(umask 004 && some command)
```

2. For systemd units `UMask` setting controls the file mode creation mask https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html#UMask=
```
[Service]
# [!!] Note that it's UMask, not umask
UMask=004
```
```shell
# Reload settings after editing a unit file
systemctl daemon-reload
```
3. For SMB shares file and directory creation masks are controlled by the following settings
```ini
[share_name]
  # Completely remove "other" permissions
  create mask = 660
  directory mask = 770
```   
4. And finally ACL mask is, as the name says, a mask that is applied to mask out permissions granted by access control entries for users and groups. It is the maximum permission that may be granted by any acccess control entry, other than by a file owner or an "other" entry. Its 3 bits are **and**ed with the 3 bits of these other entries.
* https://unix.stackexchange.com/questions/475698/what-is-the-exact-purpose-of-mask-in-file-system-acl/475796#475796
* :warning: 2check: create a testlab and check if 'other' setting overrides `umask` of a process

  ### Examples
```shell
# SMB share structure
# [!!] Make sure that 'create mask = 660' and 'directory mask = 770' options are set

# -s option sets (replaces) all ACLs
setfacl -d -R -s o::--- /shares/seafile-client
setfacl    -R -s o::--- /shares/seafile-client

setfacl -d -R mask:rwx /shares/seafile-client
setfacl    -R mask:rwx /shares/seafile-client

# no -R and -d options
setfacl -m g:smb-share-users:rx,g:smb-share-full-access:rwx /shares/seafile-client
# no write access for smb-share-full-access is intentional
setfacl -m g:smb-share-users:rx,g:smb-share-full-access:rx /shares/seafile-client/seafile

# Full access for all users
setfacl -d -R -m g:smb-share-users:rwx,g:smb-share-full-access:rwx /mnt/hdd1/seafile-client/seafile/project2
setfacl    -R -m g:smb-share-users:rwx,g:smb-share-full-access:rwx /mnt/hdd1/seafile-client/seafile/project1

# Read-only access for ordinary users
setfacl -d -R -m g:smb-share-users:rx,g:smb-share-full-access:rwx /mnt/hdd1/seafile-client/seafile/project2
setfacl    -R -m g:smb-share-users:rx,g:smb-share-full-access:rwx /mnt/hdd1/seafile-client/seafile/project2

# No access for ordinary users
setfacl -d -R -m g:smb-share-full-access:rwx /mnt/hdd1/seafile-client/seafile/project3
setfacl    -R -m g:smb-share-full-access:rwx /mnt/hdd1/seafile-client/seafile/project3
# double check resulting access list
getfacl /mnt/hdd1/seafile-client/seafile/project3
```


```shell
export acl_path=/mnt/dir
export acl_user=username

setfacl -d -R -m mask:rwx ${acl_path}
setfacl -R -m mask:rwx ${acl_path}
setfacl -d -R -m u:${acl_user}:rwx ${acl_path}
setfacl -R -m u:${acl_user}:rwx ${acl_path}
```

:bulb: Copy existing ACLs
```shell
getfacl file-or-dir1 | setfacl --set-file=- file-or-dir2
```

```shell
# set r(read) for "ubuntu" user to /home/test.txt
setfacl -m u:ubuntu:r /home/test.txt

# set r(read) for "ubuntu" to "/home/testdir" recursively
setfacl -R -m u:ubuntu:r /home/testdir

# set **DEFAULT** ACL "r-x(read/execute)" for "ubuntu" to "/home/testdir" directory
setfacl -d -m u:ubuntu:r-x /home/testdir

# remove ACL from "/home/test.txt"
setfacl -b /home/test.txt
# remove ACL only for "fedora" user on "/home/test.txt"
setfacl -x u:ubuntu /home/test.txt

# Check what is does
setfacl -m default:group::--- directory
```

:warning: Umask affects group permission
* https://serverfault.com/questions/96514/how-to-set-linux-default-acls-differently-for-directories-and-files/97854#97854
* https://stackoverflow.com/questions/33143883/why-is-umask-setting-in-etc-login-defs-not-honoured
```shell
umask
# UMASK 002
nano /etc/login.defs
```
```
setfacl -d -m mask:rwx directory
setfacl -R -d -m other::--- directory
```

#### AD domain example
:warning: 2check: capital "X" applies only to directories and not files

```shell
mkdir /share/test_dir

setfacl mask:rwx /share/test_dir
setfacl -d -m mask:rwx /share/test_dir

setfacl -m other::--- /share/test_dir
setfacl -d -m other::--- /share/test_dir

# 000 has the same effect as ---
# Could have used numerical gid instead of quoting group name
# getent group "domain users"
setfacl -m "g:domain users:000" /share/test_dir
setfacl -d -m "g:domain users:000" /share/test_dir

setfacl -m g:domain-admins:rwx /share/test_dir
setfacl -d -m g:domain-admins:rwx /share/test_dir

setfacl -m g:read-only-group:r-x /share/test_dir
setfacl -d -m g:read-only-group:r-x /share/test_dir
```
`/etc/samba/smb.conf` entry:
```
[test_dir]
    path = /share/test_dir
    public = no
    valid users = "@domain-admins", "@read-only-group"
    read list = "@domain-admins", "@read-only-group"
    write list = "@domain-admins"
```
