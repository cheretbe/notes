* https://www.server-world.info/en/note?os=Ubuntu_14.04&p=acl

:bulb: Copy existing ACLs
```shell
getfacl file-or-dir1 | setfacl --set-file=- file-or-dir2
```

```shell
apt install acl
# check for acl option
tune2fs -l /dev/sda1 | grep "Default mount options"


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
