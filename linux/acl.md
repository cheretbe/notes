* https://www.server-world.info/en/note?os=Ubuntu_14.04&p=acl

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
